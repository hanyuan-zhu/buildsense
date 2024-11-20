from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import User, Company, Project
from .serializers import UserSerializer, CompanySerializer, ProjectSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
import logging
from rest_framework import status

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny] 
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        logger.debug(f"收到登录请求: {request.data}")
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            logger.debug(f"登录成功: {username}")
            return Response(response_data)
        else:
            logger.warning(f"登录失败: {username}")
            return Response({'error': 'Invalid Credentials'}, status=400)

class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        company_id = self.kwargs['company_id']
        return Project.objects.filter(company_id=company_id)

class LogoutView(APIView):
    def post(self, request):
        try:
            logger.info("Logout request data: %s", request.data)
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error("Error during logout: %s", str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'company': user.company.name if user.company else None,
            'project': user.project.name if user.project else None,
        }
        return Response(user_data)
