# Generated by Django 5.1.2 on 2024-11-27 06:37

from django.db import migrations
from core.constants import INITIAL_COMPANIES, INITIAL_PROJECTS

def initialize_companies_and_projects(apps, schema_editor):
    Company = apps.get_model('core', 'Company')
    Project = apps.get_model('core', 'Project')

    # 初始化公司
    companies = {}
    for company_name in INITIAL_COMPANIES:
        company, created = Company.objects.get_or_create(name=company_name)
        companies[company_name] = company

    # 初始化项目
    for project_data in INITIAL_PROJECTS:
        company = companies.get(project_data['company'])
        Project.objects.get_or_create(name=project_data['name'], company=company)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_companies_and_projects),
    ]
