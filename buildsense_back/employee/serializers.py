# employee/serializers.py
from rest_framework import serializers
from .models import Employee
from core.models import Company, Project

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'position', 'company', 'project', 'employment_status', 'employment_date']
        extra_kwargs = {
            'employment_status': {'required': False},  # 确保 employment_status 字段是可选的
        }