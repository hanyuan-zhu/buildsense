# from rest_framework import serializers
# from .models import Employee, EmployeeChangeLog, Company, Project

# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = ['id', 'name']

# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['id', 'name']

# class EmployeeEntrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = ['name', 'position', 'employment_date']

# class EmployeeSerializer(serializers.ModelSerializer):
#     company = CompanySerializer(read_only=True)
#     project = ProjectSerializer(read_only=True)

#     class Meta:
#         model = Employee
#         fields = ['id', 'name', 'position', 'company', 'project', 'employment_status', 'employment_date']

# class EmployeeTransferSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmployeeChangeLog
#         fields = ['employee', 'new_company', 'new_project', 'effective_date']

#     def validate(self, attrs):
#         if not attrs.get('new_company') or not attrs.get('new_project'):
#             raise serializers.ValidationError('调岗变动需要提供新公司和新项目')
#         return attrs

#     def create(self, validated_data):
#         employee = validated_data['employee']
#         # 保存当前公司和项目作为old值 (可能为None)
#         validated_data['old_company'] = employee.company if employee.company else None
#         validated_data['old_project'] = employee.project if employee.project else None
#         validated_data['change_type'] = '调岗'
#         return super().create(validated_data)

# class EmployeeResignationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmployeeChangeLog
#         fields = ['employee', 'effective_date']

#     def validate(self, attrs):
#         if not attrs.get('employee'):
#             raise serializers.ValidationError('离职变动需要指定员工')
#         return attrs

#     def create(self, validated_data):
#         validated_data['change_type'] = '离职'
#         return super().create(validated_data)

# class EmployeeChangeLogSerializer(serializers.ModelSerializer):
#     employee = EmployeeSerializer(read_only=True)
#     old_company = CompanySerializer(read_only=True)
#     old_project = ProjectSerializer(read_only=True)
#     new_company = CompanySerializer(read_only=True)
#     new_project = ProjectSerializer(read_only=True)

#     class Meta:
#         model = EmployeeChangeLog
#         fields = '__all__'