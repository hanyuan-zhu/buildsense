# buildsense_back/permissions/migrations/0002_initialize_permissions.py

from django.db import migrations
from permissions.constants import PERMISSION_CODES, ROLE_PERMISSIONS

def initialize_permissions_and_roles(apps, schema_editor):
    Permission = apps.get_model('permissions', 'Permission')
    Role = apps.get_model('permissions', 'Role')

    # 创建权限
    permissions = {}
    for category_perms in PERMISSION_CODES.values():
        for codename in category_perms.values():
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                defaults={'name': codename.replace('_', ' ').title()}
            )
            permissions[codename] = permission

    # 创建角色并分配权限
    for role_name, perm_codenames in ROLE_PERMISSIONS.items():
        role, created = Role.objects.get_or_create(name=role_name)
        role_perms = [permissions[code] for code in perm_codenames]
        role.permissions.set(role_perms)

class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_permissions_and_roles),
    ]
