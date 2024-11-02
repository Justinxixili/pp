import json
from django.core.management.base import BaseCommand
from my_pp.models import Patent, Company
from django.conf import settings
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Import patents and companies data from JSON files'

    def parse_date(self, date_str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None

    def handle(self, *args, **options):
        # 首先清空现有数据（可选）
        Patent.objects.all().delete()
        Company.objects.all().delete()

        # 导入专利数据
        patents_file = os.path.join(settings.BASE_DIR, 'my_pp', 'data', 'patents.json')
        try:
            with open(patents_file, 'r', encoding='utf-8') as f:
                patents_data = json.load(f)
                self.stdout.write(f"Found {len(patents_data)} patents to import")

                for patent in patents_data:
                    # 打印正在处理的专利信息
                    self.stdout.write(f"Processing patent: {patent['publication_number']}")

                    # 解析 JSON 字符串字段
                    try:
                        claims = json.loads(patent['claims']) if isinstance(patent['claims'], str) else patent['claims']
                        inventors = json.loads(patent['inventors']) if isinstance(patent['inventors'], str) else patent[
                            'inventors']
                        classifications = json.loads(patent['classifications']) if isinstance(patent['classifications'],
                                                                                              str) else patent[
                            'classifications']
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(
                            f"Error parsing JSON fields for patent {patent['publication_number']}: {str(e)}"))
                        continue

                    try:
                        # 创建专利记录
                        Patent.objects.create(
                            patent_id=patent['publication_number'],
                            title=patent.get('title', ''),
                            abstract=patent.get('abstract', ''),
                            description=patent.get('description', ''),
                            assignee=patent.get('assignee', ''),
                            inventors=inventors,
                            priority_date=self.parse_date(patent.get('priority_date')),
                            application_date=self.parse_date(patent.get('application_date')),
                            grant_date=self.parse_date(patent.get('grant_date')),
                            claims=claims,
                            jurisdictions=patent.get('jurisdictions', ''),
                            classifications=classifications
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f"Successfully imported patent: {patent['publication_number']}"))
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"Error creating patent {patent['publication_number']}: {str(e)}"))
                        continue

                self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(patents_data)} patents'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing patents: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))

        # 导入公司数据
        companies_file = os.path.join(settings.BASE_DIR, 'my_pp', 'data', 'company_products.json')
        try:
            with open(companies_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                companies_data = data.get('companies', [])
                self.stdout.write(f"Found {len(companies_data)} companies to import")

                for company in companies_data:
                    try:
                        Company.objects.create(
                            name=company['name'],
                            products=company['products']
                        )
                        self.stdout.write(self.style.SUCCESS(f"Successfully imported company: {company['name']}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error creating company {company['name']}: {str(e)}"))
                        continue

                self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(companies_data)} companies'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing companies: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))

        # 打印导入结果统计
        self.stdout.write("\nImport Summary:")
        self.stdout.write(f"Patents in database: {Patent.objects.count()}")
        self.stdout.write(f"Companies in database: {Company.objects.count()}")