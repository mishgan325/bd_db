from django.shortcuts import render, redirect
from django.db import connection
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.forms import modelform_factory
from .models import *  # Импортируем все модели
from django.http import Http404
from django.contrib.auth.decorators import login_required


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
        record = get_object_or_404(model, player_id=first_key, server_id=second_key)
    elif model == CharacterAttack:
        record = get_object_or_404(model, character_id=first_key, attack_id=second_key)
    elif model == PlayerCharacterRank:
        record = get_object_or_404(model, player_id=first_key, character_id=second_key)
    else:
        record = get_object_or_404(model, id=first_key)

    # Создаем форму для этой модели
    form_class = modelform_factory(model, exclude=['id'])  # Исключаем поле 'id'
    form = form_class(instance=record)

    if request.method == 'POST':

        form = form_class(request.POST, instance=record)
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

    # Получаем запись по ID
    record = None

    if model == PlayerServer:
        record = get_object_or_404(model, player_id=first_key, server_id=second_key)
    elif model == CharacterAttack:
        record = get_object_or_404(model, character_id=first_key, attack_id=second_key)
    elif model == PlayerCharacterRank:
        record = get_object_or_404(model, player_id=first_key, character_id=second_key)
    else:
        record = get_object_or_404(model, id=first_key)

    # Удаляем запись
    if request.method == 'POST':
        record.delete()
        return redirect('table_app:list_tables')  # Перенаправление на список таблиц после удаления

    return render(request, 'table_app/confirm_delete.html', {'record': record})