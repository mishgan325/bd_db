from django.urls import path
from table_app import views


app_name = 'table_app'


urlpatterns = [
    path('', views.list_tables, name='list_tables'),
    path('<str:table_name>/', views.view_table, name='view_table'),
    path('<str:table_name>/<int:record_id>/edit/', views.edit_record, name='edit_record'),
]