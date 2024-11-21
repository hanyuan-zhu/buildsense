from django.db import models
from login.models import Company, Project
from django.contrib.auth import get_user_model

class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name='姓名')
    position = models.CharField(max_length=100, verbose_name='岗位')
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属公司')
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属项目')
    employment_status = models.CharField(
        max_length=20,
        choices=[
            ('在职', '在职'),
            ('离职', '离职'),
        ],
        default='在职',
        verbose_name='在岗状态'
    )
    employment_date = models.DateField(null=True, blank=True, verbose_name='入职日期')
    latest_position_date = models.DateField(null=True, blank=True, verbose_name='最新岗位日期')

    def __str__(self):
        return self.name

class EmployeeChangeLog(models.Model):
    CHANGE_TYPES = [
        ('调岗', '调岗'),
        ('离职', '离职'),
    ]
    STATUS_CHOICES = [
        ('待确认', '待确认'),
        ('已确认', '已确认'),
        ('已拒绝', '已拒绝'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPES, verbose_name='变动类型')
    old_company = models.ForeignKey(
        Company,
        related_name='old_company',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='原公司'
    )
    old_project = models.ForeignKey(
        Project,
        related_name='old_project',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='原项目'
    )
    new_company = models.ForeignKey(
        Company,
        related_name='new_company',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='新公司'
    )
    new_project = models.ForeignKey(
        Project,
        related_name='new_project',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='新项目'
    )
    effective_date = models.DateField(verbose_name='生效日期')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='待确认', verbose_name='状态')
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    applied_by = models.ForeignKey(
        get_user_model(),
        related_name='applied_changes',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='申请人'
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name='确认时间')
    approved_by = models.ForeignKey(
        get_user_model(),
        related_name='approved_changes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='确认人'
    )

    def __str__(self):
        return f"{self.employee.name} - {self.change_type} - {self.status}"
