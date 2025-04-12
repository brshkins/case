from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TestForm
from .models import TestResult, Profession
from django.db.models import Q

def index(request):
    return render(request, 'main/index.html')

def test1(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            answers = form.cleaned_data
            # Подсчитаем результат, например, на основе кодов (RIASEC)
            code = calculate_code(answers)  # Функция для вычисления кода
            user_name = request.POST.get('user_name', 'Anonymous')

            # Сохраняем результаты в базу данных
            test_result = TestResult.objects.create(user_name=user_name, answers=answers, code=code)

            # Получаем профессии по коду
            professions = Profession.objects.filter(Q(code__icontains=code[0]) | Q(code__icontains=code[1]) | Q(code__icontains=code[2]))

            return render(request, 'main/test1_result.html', {'professions': professions, 'user_name': user_name, 'code': code})
    else:
        form = TestForm()

    return render(request, 'main/test1.html', {'form': form})

# Функция для вычисления кода RIASEC на основе ответов
def calculate_code(answers):
    # Простая логика для примера: выбираем первые буквы ответов
    code = answers['question_1'][0] + answers['question_2'][0]  # Добавь остальные вопросы
    return code

def test2(request):
    return render(request, 'main/test2.html')

def test3(request):
    return render(request, 'main/test3.html')