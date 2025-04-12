import csv
import os
from django.core.management.base import BaseCommand
from main.models import Profession  # Правильный импорт модели

class Command(BaseCommand):
    help = 'Загружает профессии из CSV в базу данных'

    def handle(self, *args, **kwargs):
        # Путь к CSV файлу
        file_path = os.path.join(os.getcwd(), 'professions.csv')

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                code = row.get('code', '').strip()
                profession_name = row.get('profession_name', '').strip()
                main_type = row.get('main_type', '').strip()
                is_additional = row.get('is_additional', '').strip()

                # Обработка пустых значений для is_additional
                if is_additional.lower() == 'true' if is_additional else False:
                    is_additional = True
                else:
                    is_additional = False

                # Создаем или обновляем запись о профессии
                profession, created = Profession.objects.get_or_create(
                    code=code,
                    profession_name=profession_name,
                    defaults={
                        'main_type': main_type,
                        'is_additional': is_additional
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Добавлена профессия: {profession_name} ({code})'))
                else:
                    self.stdout.write(self.style.WARNING(f'Профессия {profession_name} ({code}) уже существует'))