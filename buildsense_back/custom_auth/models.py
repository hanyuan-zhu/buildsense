from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(max_length=50)
    company = models.ForeignKey('core.Company', on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey('core.Project', on_delete=models.SET_NULL, null=True, blank=True)
