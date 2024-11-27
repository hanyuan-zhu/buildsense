# from django.shortcuts import render
# from rest_framework import viewsets, permissions, generics
# from .models import Employee, EmployeeChangeLog, Company, Project
# from .serializers import (
#     EmployeeSerializer, EmployeeChangeLogSerializer,
#     EmployeeEntrySerializer, EmployeeTransferSerializer,
#     EmployeeResignationSerializer, CompanySerializer, ProjectSerializer
# )
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import status
# from django.utils import timezone
# from django.db.models import Q
# from permissions.decorators import permission_required
# from permissions.constants import PERMISSION_CODES

# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         user_permissions = self.request.user_permissions

#         if PERMISSION_CODES['employee']['view_all'] in user_permissions:
#             # 总公司管理员，查看所有员工
#             return self.queryset
#         elif PERMISSION_CODES['employee']['view_company'] in user_permissions:
#             # 公司管理员，查看本公司员工
#             return self.queryset.filter(company=user.company)
#         elif PERMISSION_CODES['employee']['view_project'] in user_permissions:
#             # 项目负责人，查看本项目员工
#             return self.queryset.filter(project=user.project)
#         else:
#             return Employee.objects.none()

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

# class EmployeeChangeLogViewSet(viewsets.ModelViewSet):
#     queryset = EmployeeChangeLog.objects.all()
#     serializer_class = EmployeeChangeLogSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         user_permissions = self.request.user_permissions
#         queryset = EmployeeChangeLog.objects.filter(status='待确认')

#         if PERMISSION_CODES['employee_change']['confirm_transfer'] in user_permissions or \
#            PERMISSION_CODES['employee_change']['confirm_resignation'] in user_permissions:
#             return queryset.filter(
#                 Q(new_company=user.company) | Q(new_project=user.project) |
#                 Q(old_company=user.company) | Q(old_project=user.project)
#             )
#         elif PERMISSION_CODES['employee']['view_all'] in user_permissions:
#             # 总公司管理员，查看所有变动
#             return queryset
#         return EmployeeChangeLog.objects.none()

#     @action(detail=True, methods=['put'])
#     @permission_required('confirm_transfer')
#     def approve_transfer(self, request, pk=None):
#         change_log = self.get_object()
#         if not self.has_approval_permission(request.user, change_log, 'transfer'):
#             return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)
#         change_log.status = '已确认'
#         change_log.approved_at = timezone.now()
#         change_log.approved_by = request.user
#         change_log.save()
#         self.update_employee(change_log)
#         return Response({'status': '已确认'}, status=status.HTTP_200_OK)

#     @action(detail=True, methods=['put'])
#     @permission_required('confirm_resignation')
#     def approve_resignation(self, request, pk=None):
#         change_log = self.get_object()
#         if not self.has_approval_permission(request.user, change_log, 'resignation'):
#             return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)
#         change_log.status = '已确认'
#         change_log.approved_at = timezone.now()
#         change_log.approved_by = request.user
#         change_log.save()
#         self.update_employee(change_log)
#         return Response({'status': '已确认'}, status=status.HTTP_200_OK)

#     def has_approval_permission(self, user, change_log, change_type):
#         user_permissions = user.user_permissions.values_list('codename', flat=True)
#         if change_type == 'transfer':
#             if PERMISSION_CODES['employee_change']['approve_company_transfer'] in user_permissions and \
#                change_log.new_company == user.company:
#                 return True
#             if PERMISSION_CODES['employee_change']['approve_project_transfer'] in user_permissions and \
#                change_log.new_project == user.project:
#                 return True
#         elif change_type == 'resignation':
#             if PERMISSION_CODES['employee_change']['confirm_resignation'] in user_permissions:
#                 return True
#         return False

#     def update_employee(self, change_log):
#         employee = change_log.employee
#         if change_log.change_type == '调岗':
#             employee.company = change_log.new_company
#             employee.project = change_log.new_project
#             employee.latest_position_date = change_log.effective_date
#             employee.save()
#         elif change_log.change_type == '离职':
#             employee.employment_status = '离职'
#             employee.company = None
#             employee.project = None
#             employee.save()

# class EmployeeEntryViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeEntrySerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         if PERMISSION_CODES['employee_change']['initiate_resignation'] not in request.user_permissions and \
#            PERMISSION_CODES['employee_change']['initiate_transfer'] not in request.user_permissions:
#             return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# class EmployeeTransferViewSet(viewsets.ModelViewSet):
#     queryset = EmployeeChangeLog.objects.filter(change_type='调岗')
#     serializer_class = EmployeeTransferSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         if PERMISSION_CODES['employee_change']['initiate_transfer'] not in request.user_permissions:
#             return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# class EmployeeResignationViewSet(viewsets.ModelViewSet):
#     queryset = EmployeeChangeLog.objects.filter(change_type='离职')
#     serializer_class = EmployeeResignationSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         if PERMISSION_CODES['employee_change']['initiate_resignation'] not in request.user_permissions:
#             return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# class CompanyListView(generics.ListAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#     permission_classes = [permissions.IsAuthenticated]

# class ProjectListView(generics.ListAPIView):
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         user_permissions = self.request.user_permissions

#         if PERMISSION_CODES['employee']['view_all'] in user_permissions:
#             return Project.objects.all()
#         elif PERMISSION_CODES['employee']['view_company'] in user_permissions:
#             return Project.objects.filter(company=user.company)
#         return Project.objects.none()
