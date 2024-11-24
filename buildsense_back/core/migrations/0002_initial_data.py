from django.db import migrations

def create_initial_data(apps, schema_editor):
    Company = apps.get_model('core', 'Company')
    Project = apps.get_model('core', 'Project')

    # 创建公司
    companies = {
        "广东财贸珠海分公司": Company.objects.create(name="广东财贸珠海分公司"),
        "联嘉": Company.objects.create(name="联嘉"),
        "广东财贸六部": Company.objects.create(name="广东财贸六部"),
        "省建筑": Company.objects.create(name="省建筑"),
        "天泽": Company.objects.create(name="天泽"),
    }

    # 创建项目
    projects = [
        {"name": "丝源大厦", "company": companies["广东财贸珠海分公司"]},
        {"name": "三灶智能制造产业园", "company": companies["联嘉"]},
        {"name": "冠宇电池厂", "company": companies["广东财贸六部"]},
        {"name": "浙江冠宇电池厂", "company": companies["广东财贸六部"]},
        {"name": "华芯半导体", "company": companies["省建筑"]},
        {"name": "红旗镇产业服务中心", "company": companies["联嘉"]},
        {"name": "广州执信花园", "company": companies["广东财贸六部"]},
        {"name": "埃克森新能源", "company": companies["联嘉"]},
        {"name": "清远涉外学院", "company": companies["广东财贸珠海分公司"]},
        {"name": "蓝领公寓", "company": companies["天泽"]},
        {"name": "保利华南总部大厦", "company": companies["广东财贸六部"]},
        {"name": "西湖湿地四期", "company": companies["广东财贸六部"]},
        {"name": "富山工业厂房", "company": companies["省建筑"]},
        {"name": "省中医院珠海分院", "company": companies["广东财贸六部"]},
        {"name": "格力创投中心", "company": companies["广东财贸珠海分公司"]},
    ]

    for project in projects:
        Project.objects.create(name=project["name"], company=project["company"])

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]