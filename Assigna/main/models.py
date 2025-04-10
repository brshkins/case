from django.db import models

class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)  # например: 'Программист', 'Дизайнер'

    def __str__(self):
        return self.text

class UserResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    answers = models.ManyToManyField(Answer)