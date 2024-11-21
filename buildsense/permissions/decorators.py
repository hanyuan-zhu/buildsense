# permissions/decorators.py
from functools import wraps
from django.core.exceptions import PermissionDenied
from .constants import PERMISSION_MAPPING

def permission_required(permission_code):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request, 'user_permissions'):
                raise PermissionDenied
            
            if permission_code not in request.user_permissions:
                raise PermissionDenied
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator