## 权限系统API参考

### 权限验证装饰器
@permission_required(permission_code)
用于视图函数的权限控制

参数:
- permission_code: 权限代码字符串

示例:
```python
@permission_required('employee.view_all')
def view_employees(request):
    pass
```

### 权限检查函数
has_permission(user, permission_code) 检查用户是否拥有指定权限
参数:
- user: User对象
- permission_code: 权限代码字符串
返回值:
- Boolean