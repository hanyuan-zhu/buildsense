# permissions/constants.py

# 权限代码定义
PERMISSION_CODES = {
    'employee': {
        'view_all': 'view_all_employees',
        'view_company': 'view_company_employees',
        'view_project': 'view_project_employees',
        'create': 'create_employee',
        'update': 'update_employee',
        'delete': 'delete_employee',
        'initiate_transfer': 'initiate_transfer',
        'confirm_transfer': 'confirm_transfer',
        'initiate_resignation': 'initiate_resignation',
        'confirm_resignation': 'confirm_resignation',
    }
}

# 角色与权限的对应关系
ROLE_PERMISSIONS = {
    '总公司管理员': [
        PERMISSION_CODES['employee']['view_all'],
        PERMISSION_CODES['employee']['create'],
        PERMISSION_CODES['employee']['update'],
        PERMISSION_CODES['employee']['delete'],
        PERMISSION_CODES['employee']['initiate_transfer'],
        PERMISSION_CODES['employee']['confirm_transfer'],
        PERMISSION_CODES['employee']['initiate_resignation'],
        PERMISSION_CODES['employee']['confirm_resignation'],
    ],
    '公司管理员': [
        PERMISSION_CODES['employee']['view_company'],
        PERMISSION_CODES['employee']['confirm_transfer'],
    ],
    '项目负责人': [
        PERMISSION_CODES['employee']['view_project'],
        PERMISSION_CODES['employee']['confirm_transfer'],
    ],
}