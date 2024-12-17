from django.shortcuts import render, redirect
from django.db import connection
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.forms import modelform_factory
from .models import *  # Импортируем все модели
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .forms import GameCharacterForm


EXCLUDED_TABLES = [
    'auth_user', 'auth_group', 'auth_permission', 'django_migrations', 
    'django_content_type', 'django_session', 'django_admin_log',
    'auth_group_permissions', 'auth_user_groups', 'auth_user_user_permissions'
]


def list_tables(request):
    """Вывод списка пользовательских таблиц в базе данных, исключая системные."""
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        all_tables = [row[0] for row in cursor.fetchall()]

    # Исключаем стандартные Django-таблицы
    user_tables = [table for table in all_tables if table not in EXCLUDED_TABLES]

    return render(request, 'table_app/list_tables.html', {'tables': user_tables})


def view_table(request, table_name):
    """Вывод данных из выбранной таблицы с пагинацией и названиями столбцов."""
    with connection.cursor() as cursor:
        # Получаем данные из выбранной таблицы
        cursor.execute(f"SELECT * FROM `{table_name}`;")
        rows = cursor.fetchall()

        # Получаем названия колонок (первый элемент из cursor.description)
        column_names = [desc[0] for desc in cursor.description]

    # Пагинация: 5 записей на страницу
    paginator = Paginator(rows, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'table_app/view_table.html', {
        'table_name': table_name,
        'columns': column_names,  # Передаем названия колонок в шаблон
        'page_obj': page_obj,  # Объект пагинации
    })


def get_model_by_name(table_name):
    # Используем Python reflection, чтобы найти модель по имени
    model_name = ''.join(tmp.capitalize() for tmp in table_name.split('_'))
    if model_name[-1] == 's':
        model_name = model_name[:-1]
    try:
        model = globals()[model_name]  # Получаем модель по имени
        return model
    except KeyError:
        raise Http404("Модель не найдена для таблицы: " + table_name, 'model_name:', model_name)


@login_required
def edit_record(request, table_name, first_key, second_key=None):
    # Получаем модель по имени таблицы
    model = get_model_by_name(table_name)

    # Получаем запись по ID
    record = None

    if model == PlayerServer:
        record = get_object_or_404(model, player=first_key, server=second_key)
    elif model == CharacterAttack:
        record = get_object_or_404(model, character=first_key, attack=second_key)
    elif model == PlayerCharacterRank:
        record = get_object_or_404(model, player=first_key, character=second_key)
    else:
        record = get_object_or_404(model, id=first_key)

    # Создаем форму для этой модели

    if model == GameCharacter:
        form_class = GameCharacterForm  # Ваша форма для GameCharacter
        print('should be unique')
    else:
        form_class = modelform_factory(model, exclude=['id'])  # Создаем форму по умолчанию для других моделей

    form = form_class(instance=record)

    if request.method == 'POST':

        form = form_class(request.POST, request.FILES, instance=record)  # Обрабатываем файлы с request.FILES
        
        if form.is_valid():
            
            if second_key:
                record.delete()
            form.save()   
            return redirect('table_app:view_table', table_name=table_name)
    
    context = {
        'form': form,
        'table_name': table_name,
        'record': record,
    }
    return render(request, 'table_app/edit_record.html', context)

@login_required
def delete_record(request, table_name, first_key, second_key=None):
    # Получаем модель по имени таблицы
    model = get_model_by_name(table_name)

    # Определяем запись
    record = None
    if model == PlayerServer:
        record = model.objects.filter(player=first_key, server=second_key).first()
    elif model == CharacterAttack:
        print('fuck db')
        record = get_object_or_404(model, character=first_key, attack=second_key)
        print("i'm here")
    elif model == PlayerCharacterRank:
        record = model.objects.filter(player=first_key, character=second_key).first()
    else:
        record = model.objects.filter(id=first_key).first()

    if not record:
        raise Http404("Запись не найдена")

    # Удаляем запись
    if request.method == 'POST':
        record.delete()
        return redirect('table_app:view_table', table_name=table_name)

    model_from_record = model_to_dict(record)

    # Передаём запись в шаблон для отображения
    return render(request, 'table_app/confirm_delete.html', {
        'record': model_from_record.values(),
        'columns': list(model_from_record.keys()),
        'table_name': table_name
    })


@login_required
def add_record(request, table_name):
    model = get_model_by_name(table_name)
    form_class = modelform_factory(model, exclude=['id'])  # Исключаем поле 'id'
    form = form_class()

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table_app:view_table', table_name=table_name)

    context = {'form': form, 'table_name': table_name}
    return render(request, 'table_app/add_record.html', context)


def count_attacks(request, character_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT count_character_attacks(%s);", [character_id])
        attack_count = cursor.fetchone()[0]  # Получаем результат функции

    return render(request, 'table_app/count_attacks.html', {'character_name': GameCharacter.objects.filter(id=character_id).first, 'attack_count': attack_count})


def attack_list(request):
    # Получаем GET параметры
    damage_min = request.GET.get('damage_min')
    damage_max = request.GET.get('damage_max')
    framedata_min = request.GET.get('framedata_min')
    framedata_max = request.GET.get('framedata_max')

    # Начальный QuerySet
    attacks = Attack.objects.all()

    # Применяем фильтры
    if damage_min:
        attacks = attacks.filter(damage__gte=damage_min)
    if damage_max:
        attacks = attacks.filter(damage__lte=damage_max)
    if framedata_min:
        attacks = attacks.filter(framedata__gte=framedata_min)
    if framedata_max:
        attacks = attacks.filter(framedata__lte=framedata_max)

    # Добавляем пагинацию
    paginator = Paginator(attacks, 6)  # 6 записей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Передаем пагинированные записи
    context = {
        'attacks': page_obj
    }
    return render(request, 'table_app/attack_list.html', context)