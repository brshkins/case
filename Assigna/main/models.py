from django.db import models

#модель для сохранения результатов
class TestResult(models.Model):
    name = models.CharField(max_length=100)
    result = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}: {self.result}"

#модель для профессий
from django.db import models


class Profession(models.Model):
    # Код RIASEC (например, "SIA", "RIA")
    code = models.CharField(max_length=10, verbose_name="Код RIASEC")

    # Название профессии
    profession_name = models.CharField(max_length=255, verbose_name="Название профессии")

    # Основной тип личности (первая буква из RIASEC)
    main_type = models.CharField(
        max_length=1,
        choices=[
            ('R', 'Realistic'),
            ('I', 'Investigative'),
            ('A', 'Artistic'),
            ('S', 'Social'),
            ('E', 'Enterprising'),
            ('C', 'Conventional')
        ],
        verbose_name="Основной тип личности",
        null=True,
        blank=True
    )

    # Дополнительная профессия или нет (для третьей буквы)
    is_additional = models.BooleanField(default=False, verbose_name="Дополнительная профессия")

    def __str__(self):
        return f"{self.profession_name} ({self.code})"