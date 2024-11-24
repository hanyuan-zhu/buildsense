from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Role
from .serializers import RoleSerializer

# Create your views here.

class RoleListView(APIView):
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response({'roles': serializer.data})
