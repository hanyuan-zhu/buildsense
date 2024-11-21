from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('head_office_admin', '总公司管理员'),
        ('company_admin', '公司管理员'),
        ('project_manager', '项目负责人'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username