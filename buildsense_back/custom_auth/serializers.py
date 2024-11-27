from rest_framework import serializers
from django.contrib.auth import get_user_model
from permissions.serializers import RoleSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'roles', 'company', 'project']

class RegisterSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role_id', 'company', 'project']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        from permissions.models import Role, UserRole  # 避免顶层导入
        
        role_id = validated_data.pop('role_id')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            company=validated_data.get('company'),
            project=validated_data.get('project'),
        )
        role = Role.objects.get(id=role_id)
        UserRole.objects.create(user=user, role=role)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()