# permissions/docs/README.md

# 权限系统开发指南

## 目录
1. 系统架构
2. 权限模型
3. 开发规范

## 1. 系统架构
- RBAC模型说明
- 组件关系图
- 数据流程图

## 2. 权限模型
### 2.1 数据模型
- Permission (权限)
- Role (角色)
- UserRole (用户-角色关联)

### 2.2 权限代码规范
格式: `<module>.<action>_<resource>`
示例: 
- employee.view_all
- project.manage
- company.approve_transfer

## 3. 开发规范
### 3.1 添加新权限
```python
# 在 permissions/constants.py 中定义
PERMISSION_CODES = {
    'employee': {
        'view_all': '查看所有员工',
        'manage': '管理员工信息',
    }
}
```

### 3.2 使用装饰器
```python
@permission_required('employee.view_all')
def view_function(request):
    pass
```

### 3.3 权限检查
```python
if request.user.has_permission('employee.manage'):
    # 执行操作
```