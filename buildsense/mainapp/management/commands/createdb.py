from django.core.management.base import BaseCommand
from django.db import connections
from django.conf import settings
import pymysql
pymysql.install_as_MySQLdb()

class Command(BaseCommand):
    help = 'Create database if it does not exist'

    def handle(self, *args, **options):
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        try:
            # 尝试连接数据库
            db = connections['default']
            c = db.cursor()
            c.close()
            self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' already exists."))
        except pymysql.OperationalError:
            # 数据库不存在，创建数据库
            self.stdout.write(f"Database '{db_name}' does not exist. Creating...")
            connection = pymysql.connect(
                host=db_settings['HOST'],
                user=db_settings['USER'],
                password=db_settings['PASSWORD'],
                port=int(db_settings['PORT'])
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cursor.close()
            connection.close()
            self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' created successfully."))