from django.db import models

class Profession(models.Model):
    code = models.CharField(max_length=3)  # Например: "SIA"
    profession_name = models.CharField(max_length=100)  # Название профессии
    is_additional = models.BooleanField(default=False)  # Дополнительная профессия

    def __str__(self):
        return self.profession_name


class TestResult(models.Model):
    code = models.CharField(max_length=3)  # Сгенерированный RIASEC-код
    professions = models.ManyToManyField(Profession)  # Привязанные профессии
    timestamp = models.DateTimeField(auto_now_add=True)  # Когда проходили тест

    def __str__(self):
        return f"Код: {self.code} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"