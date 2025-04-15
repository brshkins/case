from .forms import TestForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Profession, TestResult
from collections import defaultdict
from django.shortcuts import render, redirect
from collections import Counter
from .models import Profession, TestResult
from collections import defaultdict
from .models import MBTIResult
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import AIQuestionnaireResult
from yandex_neural_api.client import YandexNeuralAPIClient
import logging
import re
import os

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

MBTI_QUESTIONS = [
    {"text": "Вам легче отдохнуть:", "dimension": "EI", "option_a": "В компании людей", "option_b": "В одиночестве"},
    {"text": "Вы чаще говорите:", "dimension": "EI", "option_a": "Сначала говорю, потом думаю", "option_b": "Думаю, прежде чем говорить"},
    {"text": "Что приносит больше удовольствия:", "dimension": "EI", "option_a": "Общение, мероприятия", "option_b": "Спокойные хобби"},
    {"text": "Вы больше доверяете:", "dimension": "SN", "option_a": "Практическому опыту", "option_b": "Интуиции и идеям"},
    {"text": "Вам ближе:", "dimension": "SN", "option_a": "Проверенные решения", "option_b": "Эксперименты, новизна"},
    {"text": "Какой стиль мышления ближе:", "dimension": "SN", "option_a": "Конкретный и реалистичный", "option_b": "Абстрактный и образный"},
    {"text": "Вы принимаете решения, основываясь на:", "dimension": "TF", "option_a": "Логике", "option_b": "Чувствах"},
    {"text": "Вам ближе:", "dimension": "TF", "option_a": "Справедливость и анализ", "option_b": "Сочувствие и гармония"},
    {"text": "В конфликте вы:", "dimension": "TF", "option_a": "Анализируете", "option_b": "Сопереживаете"},
    {"text": "Вы чаще:", "dimension": "JP", "option_a": "Планируете заранее", "option_b": "Действуете спонтанно"},
    {"text": "Вам ближе:", "dimension": "JP", "option_a": "Чёткий график", "option_b": "Свобода и гибкость"},
    {"text": "При работе вы:", "dimension": "JP", "option_a": "Завершаете начатое", "option_b": "Легко переключаетесь"},
]

MBTI_TYPES = {
    'ISTJ': {
        'description': 'Организованный, ответственный, практичный. Любите стабильность и планирование.',
        'professions': ['Бухгалтер', 'Аналитик данных', 'Администратор', 'Инженер']
    },
    'ISFJ': {
        'description': 'Заботливый, надёжный, трудолюбивый. Сосредоточены на помощи другим.',
        'professions': ['Учитель', 'Медсестра', 'Социальный работник', 'Архивариус']
    },
    'INFJ': {
        'description': 'Идеалист, интуитивный и глубоко чувствующий. Часто вдохновляете других.',
        'professions': ['Психолог', 'Писатель', 'Коуч', 'Арт-терапевт']
    },
    'INTJ': {
        'description': 'Стратег, любит планировать и анализировать. Независим и уверен в себе.',
        'professions': ['Программист', 'Инженер', 'Научный сотрудник', 'Стратег']
    },
    'ISTP': {
        'description': 'Практичный, логичный, независимый. Любите работать руками и решать задачи.',
        'professions': ['Механик', 'Инженер', 'Спасатель', 'Техник']
    },
    'ISFP': {
        'description': 'Спокойный, доброжелательный, чувствительный. Тянетесь к красоте и искусству.',
        'professions': ['Флорист', 'Фотограф', 'Дизайнер интерьеров', 'Иллюстратор']
    },
    'INFP': {
        'description': 'Идеалистичный, мечтательный, цените гармонию. Вас вдохновляют идеи.',
        'professions': ['Писатель', 'Редактор', 'Психолог', 'Преподаватель гуманитарных наук']
    },
    'INTP': {
        'description': 'Аналитик, любознательный и независимый. Предпочитаете глубокое мышление.',
        'professions': ['Научный исследователь', 'Программист', 'Теоретик', 'Системный аналитик']
    },
    'ESTP': {
        'description': 'Энергичный, практичный, решительный. Любите действия и вызовы.',
        'professions': ['Предприниматель', 'Спортивный тренер', 'Менеджер по продажам', 'Спасатель']
    },
    'ESFP': {
        'description': 'Общительный, энергичный, жизнерадостный. Любите быть в центре внимания.',
        'professions': ['Актёр', 'Стилист', 'Организатор мероприятий', 'Ведущий']
    },
    'ENFP': {
        'description': 'Творческий, вдохновляющий, эмоциональный. Ищете смысл в жизни и работе.',
        'professions': ['Маркетолог', 'Журналист', 'Тренер', 'Педагог']
    },
    'ENTP': {
        'description': 'Изобретательный, остроумный, любит споры. Вам интересны новые идеи.',
        'professions': ['Стартапер', 'PR-специалист', 'Разработчик продуктов', 'Политолог']
    },
    'ESTJ': {
        'description': 'Практичный, решительный, организованный. Цените эффективность и структуру.',
        'professions': ['Менеджер', 'Полицейский', 'Логист', 'Проектный координатор']
    },
    'ESFJ': {
        'description': 'Дружелюбный, надёжный, ориентированный на других. Стремитесь помогать.',
        'professions': ['Учитель', 'HR-менеджер', 'Фармацевт', 'Консультант']
    },
    'ENFJ': {
        'description': 'Лидер, вдохновляющий, заботливый. Умеете объединять людей.',
        'professions': ['Психолог', 'Тренер', 'Координатор проектов', 'Лектор']
    },
    'ENTJ': {
        'description': 'Амбициозный, стратегический, уверенный. Прирождённый руководитель.',
        'professions': ['Руководитель', 'Бизнес-аналитик', 'Адвокат', 'IT-директор']
    }
}

def index(request):
    return render(request, 'main/index.html')

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

def test1_result(request, result_id):
    result = TestResult.objects.get(id=result_id)
    professions = result.professions.all()
    if result.code:
        type_description = RIASEC_DESCRIPTIONS.get(result.code[0], '')
    else:
        type_description = 'Тип личности не определён'
    return render(request, 'main/test1_result.html', {
        'riasec_code': result.code,
        'professions': professions,
        'type_description': type_description
    })


def test2(request):
    if request.method == 'POST':
        scores = defaultdict(int)

        for i in range(1, 13):
            answer = request.POST.get(f'answer_{i}')
            dimension = request.POST.get(f'dimension_{i}')
            if not answer or not dimension:
                continue
            if answer == 'A':
                scores[dimension[0]] += 1
            else:
                scores[dimension[1]] += 1

        # Генерация кода по 4 шкалам
        code = ''
        for pair in ['EI', 'SN', 'TF', 'JP']:
            if scores[pair[0]] > scores[pair[1]]:
                code += pair[0]
            else:
                code += pair[1]  # если равны, выбираем вторую букву

        info = MBTI_TYPES.get(code, {
            'description': 'Описание не найдено.',
            'professions': ['Профессии не найдены']
        })

        MBTIResult.objects.create(code=code, description=info['description']) #сохраняем результат в БД

        return render(request, 'main/test2_result.html', {
            'mbti_code': code,
            'description': info['description'],
            'professions': info['professions']
        })

    return render(request, 'main/test2.html', {'questions': MBTI_QUESTIONS})

def test2_result(request, result_id):
    return render(request, 'main/test2_result.html', {})

# Настройки подключения к Yandex GPT
client = YandexNeuralAPIClient(
    iam_token=os.getenv("YANDEX_IAM_TOKEN"),
    folder_id=os.getenv("YANDEX_FOLDER_ID")
)

# Вопросы + анализ по GPT
def test3(request):
    if request.method == 'GET':
        prompt = (
            "Сгенерируй 5 коротких вопросов по профориентации, каждый с 3–4 вариантами ответов. "
            "Верни только JSON-массив: [{\"question\": \"...\", \"options\": [\"...\", \"...\"]}, ...]"
        )

        try:
            raw_response = client.generate_text(prompt)
            print(f'ответ от YandexGPT: \n {raw_response}')

            cleaned_response = re.search(r"\[.*\]", raw_response, re.DOTALL)
            if not cleaned_response:
                return render(request, 'main/test3_error.html', {"error": "Ответ ИИ не содержит JSON-массив"})

            questions = json.loads(cleaned_response.group(0))
        except Exception as e:
            return render(request, 'main/test3_error.html', {"error": str(e)})

        return render(request, 'main/test3.html', {'questions': questions})

    elif request.method == 'POST':
        answers = {}
        for key, value in request.POST.items():
            if key.startswith("answer_"):
                answers[key] = value

        formatted_answers = "\n".join([f"{k}: {v}" for k, v in answers.items()])

        analysis_prompt = (
            f"Пользователь ответил так:\n{formatted_answers}\n\n"
            "Сделай вывод о типе личности, опиши его кратко, и предложи список из 3–5 профессий. "
            "Верни только JSON, без пояснений: {\"type\": \"...\", \"description\": \"...\", \"professions\": [\"...\", ...]}"
        )
        print('prompt для анализа: \n', analysis_prompt)

        try:
            result_raw = client.generate_text(analysis_prompt)
            print(f'ответ от GPT: \n {result_raw}')
            result_data = json.loads(result_raw.strip('` \n'))
        except Exception as e:
            return render(request, 'main/test3_error.html', {"error": str(e)})

        result = AIQuestionnaireResult.objects.create(
            answers=answers,
            result_type=result_data.get("type", "Не определён"),
            description=result_data.get("description", ""),
            professions=result_data.get("professions", [])
        )

        print('ответы:', answers)
        print('результат от гпт:', result_data)
        return redirect('test3_result', result_id=result.id)

# Отображение результата
def test3_result(request, result_id):
    result = AIQuestionnaireResult.objects.get(id=result_id)
    return render(request, 'main/test3_result.html', {'result': result})
