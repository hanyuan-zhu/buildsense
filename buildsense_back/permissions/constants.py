# permissions/constants.py
PERMISSION_MAPPING = {
    'employee_view': {
        'head_office_admin': ['view_all_employees'],
        'company_admin': ['view_company_employees'],
        'project_manager': ['view_project_employees']
    },
    'employee_change': {
        'head_office_admin': [
            'create_employee',
            'update_employee',
            'delete_employee',
            'initiate_transfer',
            'confirm_transfer',
            'initiate_resignation',
            'confirm_resignation'
        ],
        'company_admin': ['approve_company_transfer'],
        'project_manager': ['approve_project_transfer']
    }
}

PERMISSION_CODES = {
    'employee': {
        'view_all': 'view_all_employees',
        'view_company': 'view_company_employees',
        'view_project': 'view_project_employees',
        'create': 'create_employee',
        'update': 'update_employee',
        'delete': 'delete_employee',
    },
    'employee_change': {
        'initiate_transfer': 'initiate_transfer',
        'confirm_transfer': 'confirm_transfer',
        'initiate_resignation': 'initiate_resignation',
        'confirm_resignation': 'confirm_resignation',
        'approve_company_transfer': 'approve_company_transfer',
        'approve_project_transfer': 'approve_project_transfer',
    },
}