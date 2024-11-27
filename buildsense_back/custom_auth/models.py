from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # roles 字段会通过 Role 模型的 related_name 自动创建
    company = models.ForeignKey('core.Company', on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey('core.Project', on_delete=models.SET_NULL, null=True, blank=True)
