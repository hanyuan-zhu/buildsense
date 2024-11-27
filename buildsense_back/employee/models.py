# employee/models.py
from django.db import models
from core.models import Company, Project

class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name='姓名')
    position = models.CharField(max_length=100, verbose_name='岗位')
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属公司')
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属项目')
    employment_status = models.CharField(
        max_length=20,
        choices=[
            ('在岗', '在岗'),
            ('待岗', '待岗'),
            ('离职', '离职'),
        ],
        default='待岗',
        verbose_name='在岗状态'
    )
    employment_date = models.DateField(null=True, blank=True, verbose_name='入职日期')
    latest_position_date = models.DateField(null=True, blank=True, verbose_name='最新岗位日期')

    def __str__(self):
        return self.name
