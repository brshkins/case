import csv
import os
from django.core.management.base import BaseCommand
from main.models import Profession

class Command(BaseCommand):
    help = 'Загружает профессии из CSV в базу данных'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.getcwd(), 'professions.csv')

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0

            for row in reader:
                code = row['code'].strip()
                name = row['profession_name'].strip()
                is_additional = row['is_additional'].strip().lower() == 'true'

                profession, created = Profession.objects.get_or_create(
                    code=code,
                    profession_name=name,
                    defaults={'is_additional': is_additional}
                )

                if created:
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'Загружено профессий: {count}'))