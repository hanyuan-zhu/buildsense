from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.cache import cache
from .models import Role
from .serializers import RoleSerializer

# Create your views here.

class RoleListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        cache_key = 'roles_list'
        cached_roles = cache.get(cache_key)
        
        if cached_roles is None:
            roles = Role.objects.prefetch_related('permissions').all()
            serializer = RoleSerializer(roles, many=True)
            cached_roles = serializer.data
            cache.set(cache_key, cached_roles, 3600)  # 缓存1小时
            
        return Response({'roles': cached_roles})
