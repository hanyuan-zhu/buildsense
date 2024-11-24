from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Company, Project
from .serializers import CompanySerializer, ProjectSerializer

class CompanyListView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response({'companies': serializer.data})

class ProjectListView(APIView):
    def get(self, request, company_id):
        projects = Project.objects.filter(company_id=company_id)
        serializer = ProjectSerializer(projects, many=True)
        return Response({'projects': serializer.data})

