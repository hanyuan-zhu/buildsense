from rest_framework.permissions import BasePermission

class IsHeadOfficeAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'head_office_admin'

class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'company_admin'

class IsProjectManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'project_manager'