from django.core.management.base import BaseCommand
from permissions.models import Permission
from permissions.constants import PERMISSION_CODES

class Command(BaseCommand):
    help = '同步 constants.py 中的权限到数据库'

    def handle(self, *args, **kwargs):
        # 获取所有权限 codename
        all_permission_codenames = set()
        for perms in PERMISSION_CODES.values():
            all_permission_codenames.update(perms.values())

        # 数据库中已有的权限
        existing_permissions = Permission.objects.values_list('codename', flat=True)

        # 找出需要添加的权限
        to_add = all_permission_codenames - set(existing_permissions)

        for codename in to_add:
            Permission.objects.create(
                codename=codename,
                name=codename.replace('_', ' ').title()
            )
            self.stdout.write(self.style.SUCCESS(f'添加权限：{codename}'))

        self.stdout.write(self.style.SUCCESS('权限同步完成。'))