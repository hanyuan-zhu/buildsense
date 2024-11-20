from django.core.management.base import BaseCommand
from mainapp.models import Company, Project
import json

class Command(BaseCommand):
    help = '导入初始的公司和项目数据'

    def handle(self, *args, **kwargs):
        # 导入公司数据
        companies_data = [
            {"公司名称": "联嘉"},
            {"公司名称": "六部"},
            {"公司名称": "省建筑"},
            {"公司名称": "珠海分公司"},
            {"公司名称": "天泽"}
        ]

        # 存储公司名称到ID的映射
        company_map = {}
        
        # 创建公司记录
        for company_data in companies_data:
            company_name = company_data["公司名称"]
            company, created = Company.objects.get_or_create(name=company_name)
            company_map[company_name] = company
            if created:
                self.stdout.write(f'创建公司: {company_name}')
            else:
                self.stdout.write(f'公司已存在: {company_name}')

        # 导入项目数据
        projects_data = [
            {"项目名称": "蓝领公寓", "公司名称": "天泽"},
            {"项目名称": "三灶智能制造产业园", "公司名称": "联嘉"},
            {"项目名称": "冠宇电池厂", "公司名称": "六部"},
            {"项目名称": "浙江冠宇电池厂", "公司名称": "六部"},
            {"项目名称": "华芯半导体", "公司名称": "省建筑"},
            {"项目名称": "红旗镇产业服务中心", "公司名称": "联嘉"},
            {"项目名称": "广州执信花园", "公司名称": "六部"},
            {"项目名称": "埃克森新能源", "公司名称": "联嘉"},
            {"项目名称": "清远涉外学院", "公司名称": "珠海分公司"},
            {"项目名称": "保利华南总部大厦", "公司名称": "六部"},
            {"项目名称": "西湖湿地四期", "公司名称": "六部"},
            {"项目名称": "富山工业厂房", "公司名称": "省建筑"},
            {"项目名称": "省中医院珠海分院", "公司名称": "六部"},
            {"项目名称": "格力创投中心", "公司名称": "珠海分公司"}
        ]

        # 创建项目记录
        for project_data in projects_data:
            project_name = project_data["项目名称"]
            company_name = project_data["公司名称"]
            
            if company_name in company_map:
                company = company_map[company_name]
                project, created = Project.objects.get_or_create(
                    name=project_name,
                    company=company
                )
                if created:
                    self.stdout.write(f'创建项目: {project_name} (公司: {company_name})')
                else:
                    self.stdout.write(f'项目已存在: {project_name} (公司: {company_name})')
            else:
                self.stdout.write(f'警告: 找不到公司 {company_name} 对应的项目 {project_name}')