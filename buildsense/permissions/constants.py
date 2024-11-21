# permissions/constants.py
PERMISSION_MAPPING = {
    'employee_view': {
        'head_office_admin': ['view_all_employees'],
        'company_admin': ['view_company_employees'],
        'project_manager': ['view_project_employees']
    },
    'employee_change': {
        'head_office_admin': ['create_employee', 'update_employee', 'delete_employee'],
        'company_admin': ['approve_company_transfer'],
        'project_manager': ['approve_project_transfer']
    }
}