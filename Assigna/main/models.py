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

class MBTIResult(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=4)
    description = models.TextField()

    def __str__(self):
        return f"{self.code} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"

class AIQuestionnaireResult(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField()  # ответы пользователя
    result_type = models.CharField(max_length=100)  # тип личности или интересов
    description = models.TextField()  # интерпретация
    professions = models.JSONField()  # список подходящих профессий

    def __str__(self):
        return f"{self.result_type} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"

