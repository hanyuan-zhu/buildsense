from django.db import migrations

def initialize_roles(apps, schema_editor):
    Role = apps.get_model('permissions', 'Role')
    Permission = apps.get_model('permissions', 'Permission')

    # 创建权限
    permissions = {
        'view_all_employees': Permission.objects.create(name='查看所有员工', codename='view_all_employees'),
        'view_company_employees': Permission.objects.create(name='查看公司员工', codename='view_company_employees'),
        'view_project_employees': Permission.objects.create(name='查看项目员工', codename='view_project_employees'),
        'create_employee': Permission.objects.create(name='创建员工', codename='create_employee'),
        'update_employee': Permission.objects.create(name='更新员工', codename='update_employee'),
        'delete_employee': Permission.objects.create(name='删除员工', codename='delete_employee'),
        'initiate_transfer': Permission.objects.create(name='发起调岗', codename='initiate_transfer'),
        'confirm_transfer': Permission.objects.create(name='确认调岗', codename='confirm_transfer'),
        'initiate_resignation': Permission.objects.create(name='发起离职', codename='initiate_resignation'),
        'confirm_resignation': Permission.objects.create(name='确认离职', codename='confirm_resignation'),
    }

    # 创建角色并分配权限
    roles = {
        '总公司管理员': Role.objects.create(name='总公司管理员'),
        '公司管理员': Role.objects.create(name='公司管理员'),
        '项目负责人': Role.objects.create(name='项目负责人'),
    }

    roles['总公司管理员'].permissions.set(permissions.values())
    roles['公司管理员'].permissions.set([
        permissions['view_company_employees'],
        permissions['confirm_transfer'],
    ])
    roles['项目负责人'].permissions.set([
        permissions['view_project_employees'],
        permissions['confirm_transfer'],
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_roles),
    ]