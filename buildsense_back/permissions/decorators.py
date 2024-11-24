# permissions/decorators.py
from functools import wraps
from django.core.exceptions import PermissionDenied
from .services import get_user_permissions

def permission_required(permission_codename):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_permissions = get_user_permissions(request.user)
            if permission_codename not in user_permissions:
                raise PermissionDenied("您没有执行此操作的权限。")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator