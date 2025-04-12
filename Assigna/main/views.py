from django.shortcuts import render
from .forms import TestForm
import json
from collections import Counter
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Profession, TestResult

from django.shortcuts import render, redirect
from collections import Counter
from .models import Profession, TestResult

# Список вопросов в виде словаря
QUESTIONS = {
    1: {"text": "Ты любишь чинить технику?", "letter": "R"},
    2: {"text": "Тебе нравится разбираться в причинах явлений?", "letter": "I"},
    3: {"text": "Ты получаешь удовольствие от рисования или музыки?", "letter": "A"},
    4: {"text": "Ты заботишься о людях и хочешь им помогать?", "letter": "S"},
    5: {"text": "Ты умеешь убеждать и вести за собой?", "letter": "E"},
    6: {"text": "Ты любишь порядок и точные инструкции?", "letter": "C"},
    7: {"text": "Тебе интересны механизмы и инструменты?", "letter": "R"},
    8: {"text": "Ты предпочитаешь проводить исследования?", "letter": "I"},
    9: {"text": "Ты любишь придумывать новое и экспериментировать?", "letter": "A"},
    10: {"text": "Ты хочешь работать с людьми и их эмоциями?", "letter": "S"},
    11: {"text": "Тебе интересно управлять проектами и бизнесом?", "letter": "E"},
    12: {"text": "Тебе нравится заполнять таблицы и документы?", "letter": "C"},
}

RIASEC_DESCRIPTIONS = {
    'R': 'Практический — ты любишь работать руками, техникой, механизмами.',
    'I': 'Исследовательский — тебе интересно анализировать и изучать.',
    'A': 'Артистичный — ты тянешься к творчеству, искусству, выражению.',
    'S': 'Социальный — ты хочешь помогать, работать с людьми.',
    'E': 'Предпринимательский — ты лидер, стремишься организовывать.',
    'C': 'Конвенциональный — тебе важны порядок, точность, структура.',
}

def test1(request):
    if request.method == 'POST':
        selected_letters = []

        for i in range(1, 13):
            answer = request.POST.get(f'answer_{i}')
            letter = request.POST.get(f'letter_{i}')
            if answer == 'Да':
                selected_letters.append(letter)

        counter = Counter(selected_letters)
        code = ''.join([x[0] for x in counter.most_common(3)])

        lead = Profession.objects.filter(code=code, is_additional=False)
        extra = Profession.objects.filter(code=code, is_additional=True).first()

        result = TestResult.objects.create(code=code)
        result.professions.set(list(lead) + ([extra] if extra else []))

        return redirect('test1_result', result_id=result.id)

    return render(request, 'main/test1.html', {'questions': QUESTIONS})

def index(request):
    return render(request, 'main/index.html')

def test2(request):
    return render(request, 'main/test2.html')

def test3(request):
    return render(request, 'main/test3.html')

def test1_result(request, result_id):
    result = TestResult.objects.get(id=result_id)
    professions = result.professions.all()
    type_description = RIASEC_DESCRIPTIONS.get(result.code[0], '')
    return render(request, 'main/test1_result.html', {
        'riasec_code': result.code,
        'professions': professions,
        'type_description': type_description
    })