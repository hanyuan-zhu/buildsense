from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Permission(models.Model):
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserRole',
        related_name='roles'
    )

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'role']
