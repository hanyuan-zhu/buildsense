from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Employee, EmployeeChangeLog, Company, Project
from .serializers import EmployeeSerializer, EmployeeChangeLogSerializer, EmployeeEntrySerializer, EmployeeTransferSerializer, EmployeeResignationSerializer, CompanySerializer, ProjectSerializer
from .permissions import IsHeadOfficeAdmin, IsCompanyAdmin, IsProjectManager
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from login.models import Company, Project
from django.db.models import Q  # 添加这行

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(f"User: {user}, Role: {user.role}, Company: {user.company}, Project: {user.project}")
        if user.role == 'head_office_admin':
            return Employee.objects.all()
        elif user.role == 'company_admin':
            queryset = Employee.objects.filter(company=user.company)
            print(f"Queried Employees: {queryset.count()}")
            return queryset
        elif user.role == 'project_manager':
            queryset = Employee.objects.filter(project=user.project)
            print(f"Queried Employees: {queryset.count()}")
            return queryset
        else:
            return Employee.objects.none()

    def list(self, request, *args, **kwargs):
        print("Employee list endpoint called")
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class EmployeeChangeLogViewSet(viewsets.ModelViewSet):
    queryset = EmployeeChangeLog.objects.all()
    serializer_class = EmployeeChangeLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = EmployeeChangeLog.objects.filter(status='待确认')

        if user.role == 'head_office_admin':
            return queryset
        elif user.role == 'company_admin':
            return queryset.filter(
                Q(new_company=user.company) |
                Q(old_company=user.company, old_company__isnull=False)
            )
        elif user.role == 'project_manager':
            return queryset.filter(
                Q(new_project=user.project) |
                Q(old_project=user.project, old_project__isnull=False)
            )
        return EmployeeChangeLog.objects.none()

    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        change_log = self.get_object()
        if not self.has_approval_permission(request.user, change_log):
            return Response(status=status.HTTP_403_FORBIDDEN)
        change_log.status = '已确认'
        change_log.approved_at = timezone.now()
        change_log.approved_by = request.user
        change_log.save()
        self.update_employee(change_log)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        change_log = self.get_object()
        if not self.has_approval_permission(request.user, change_log):
            return Response(status=status.HTTP_403_FORBIDDEN)
        change_log.status = '已拒绝'
        change_log.approved_at = timezone.now()
        change_log.approved_by = request.user
        change_log.save()
        return Response(status=status.HTTP_200_OK)

    def has_approval_permission(self, user, change_log):
        # 只有新单位有权限操作
        if user.role == 'head_office_admin':
            return True
        if user.role == 'company_admin':
            return change_log.new_company == user.company
        if user.role == 'project_manager':
            return change_log.new_project == user.project
        return False

    def update_employee(self, change_log):
        employee = change_log.employee
        if change_log.change_type == '调岗':
            employee.company = change_log.new_company
            employee.project = change_log.new_project
            employee.latest_position_date = change_log.effective_date
            employee.save()
        elif change_log.change_type == '离职':
            employee.employment_status = '离职'
            employee.company = None
            employee.project = None
            employee.save()

class EmployeeEntryViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsHeadOfficeAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EmployeeTransferViewSet(viewsets.ModelViewSet):
    queryset = EmployeeChangeLog.objects.filter(change_type='调岗')
    serializer_class = EmployeeTransferSerializer
    permission_classes = [permissions.IsAuthenticated, IsHeadOfficeAdmin]

class EmployeeResignationViewSet(viewsets.ModelViewSet):
    queryset = EmployeeChangeLog.objects.filter(change_type='离职')
    serializer_class = EmployeeResignationSerializer
    permission_classes = [permissions.IsAuthenticated, IsHeadOfficeAdmin]

class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        return Project.objects.filter(company_id=company_id)
