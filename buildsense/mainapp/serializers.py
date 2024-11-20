from rest_framework import serializers
from .models import User, Company, Project

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'role', 'company', 'project')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role'),
            company=validated_data.get('company'),
            project=validated_data.get('project'),
        )
        return user

class CompanySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='name') 
    
    class Meta:
        model = Company
        fields = ['id', 'company_name']  

class ProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='name')  
    
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'company']
