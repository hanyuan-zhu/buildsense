# permissions/services.py
from .models import Permission, UserRole
from django.core.cache import cache

def get_user_permissions(user):
    cache_key = f'user_permissions_{user.id}'
    permissions = cache.get(cache_key)
    
    if permissions is None:
        roles = UserRole.objects.filter(user=user).select_related('role')
        permissions = set()
        for user_role in roles:
            role_perms = user_role.role.permissions.values_list('codename', flat=True)
            permissions.update(role_perms)
        cache.set(cache_key, permissions, 3600)  # 缓存1小时
    
    return permissions