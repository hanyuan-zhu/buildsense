from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response  # 导入 Response
from .models import Employee
from .serializers import EmployeeSerializer
from permissions.constants import PERMISSION_CODES

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_permissions = self.request.user_permissions

        print(f"User: {user}, Permissions: {user_permissions}")  # 打印用户和权限信息

        if PERMISSION_CODES['employee']['view_all'] in user_permissions:
            # 总公司管理员，查看所有员工
            queryset = self.queryset.filter(employment_status__in=['在岗', '待岗'])
            print(queryset.query)  # 打印 SQL 查询语句
            return queryset
        elif PERMISSION_CODES['employee']['view_company'] in user_permissions:
            # 公司管理员，查看本公司员工
            queryset = self.queryset.filter(company=user.company, employment_status__in=['在岗', '待岗'])
            print(queryset.query)  # 打印 SQL 查询语句
            return queryset
        elif PERMISSION_CODES['employee']['view_project'] in user_permissions:
            # 项目负责人，查看本项目员工
            queryset = self.queryset.filter(project=user.project, employment_status__in=['在岗', '待岗'])
            print(queryset.query)  # 打印 SQL 查询语句
            return queryset
        else:
            return Employee.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset.query)  # 打印 SQL 查询语句
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
