# permissions/middleware.py
from django.utils.functional import SimpleLazyObject
from .services import get_user_permissions

class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            request.user_permissions = SimpleLazyObject(
                lambda: get_user_permissions(request.user)
            )
        return self.get_response(request)