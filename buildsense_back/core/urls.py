# buildsense_back/core/urls.py
from django.urls import path
from .views import CompanyListView, ProjectListView

urlpatterns = [
    path('companies', CompanyListView.as_view(), name='company-list'),
    path('companies/<int:company_id>/projects', ProjectListView.as_view(), name='project-list'),
]