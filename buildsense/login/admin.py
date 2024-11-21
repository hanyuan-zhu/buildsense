from django.contrib import admin
from .models import User, Company, Project

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Project)

# Register your models here.
