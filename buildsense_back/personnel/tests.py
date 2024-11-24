from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import Company, Project
from custom_auth.models import User
from .models import Employee

class EmployeeListViewTest(TestCase):
    def setUp(self):
        # 创建公司
        self.company1 = Company.objects.create(name='公司A')
        self.company2 = Company.objects.create(name='公司B')

        # 创建项目
        self.project1 = Project.objects.create(name='项目A1', company=self.company1)
        self.project2 = Project.objects.create(name='项目B1', company=self.company2)

        # 创建员工
        Employee.objects.create(name='员工1', position='职位1', company=self.company1, project=self.project1, employment_status='在岗')
        Employee.objects.create(name='员工2', position='职位2', company=self.company2, project=self.project2, employment_status='离职')

        # 创建用户
        self.head_admin = User.objects.create_user(username='head_admin', password='pass', role='head_office_admin')
        self.company_admin = User.objects.create_user(username='company_admin', password='pass', role='company_admin', company=self.company1)
        self.project_manager = User.objects.create_user(username='project_manager', password='pass', role='project_manager', project=self.project1)

        # 创建API客户端，用于模拟HTTP请求
        self.client = APIClient()

    def get_token(self, username, password):
        # 获取JWT令牌
        response = self.client.post(reverse('token_obtain_pair'), {'username': username, 'password': password})
        return response.data['access']

    def test_head_office_admin_can_view_all_employees(self):
        # 获取head_office_admin用户的JWT令牌
        token = self.get_token('head_admin', 'pass')
        # 设置HTTP请求头，包含JWT令牌
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # 发送GET请求到employee-list视图
        response = self.client.get(reverse('employee-list'))
        # 断言响应状态码为200（成功）
        self.assertEqual(response.status_code, 200)
        # 断言返回的员工数量为2
        self.assertEqual(len(response.data), 2)

    def test_company_admin_can_view_company_employees(self):
        # 获取company_admin用户的JWT令牌
        token = self.get_token('company_admin', 'pass')
        # 设置HTTP请求头，包含JWT令牌
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # 发送GET请求到employee-list视图
        response = self.client.get(reverse('employee-list'))
        # 断言响应状态码为200（成功）
        self.assertEqual(response.status_code, 200)
        # 断言返回的员工数量为1
        self.assertEqual(len(response.data), 1)
        # 断言返回的员工所属公司为公司A
        self.assertEqual(response.data[0]['company']['name'], '公司A')

    def test_project_manager_can_view_project_employees(self):
        # 获取project_manager用户的JWT令牌
        token = self.get_token('project_manager', 'pass')
        # 设置HTTP请求头，包含JWT令牌
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # 发送GET请求到employee-list视图
        response = self.client.get(reverse('employee-list'))
        # 断言响应状态码为200（成功）
        self.assertEqual(response.status_code, 200)
        # 断言返回的员工数量为1
        self.assertEqual(len(response.data), 1)
        # 断言返回的员工所属项目为项目A1
        self.assertEqual(response.data[0]['project']['name'], '项目A1')
