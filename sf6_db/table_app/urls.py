from django.urls import path
from table_app import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'table_app'

urlpatterns = [
    # Для входа:
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # Для выхода:
    path('logout/', auth_views.LogoutView.as_view(next_page='table_app:list_tables'), name='logout'),
    path('attacks/', views.attack_list, name='attack_list'),
    path('', views.list_tables, name='list_tables'),
    path('<str:table_name>/', views.view_table, name='view_table'),
    path('<str:table_name>/<int:first_key>/edit/', views.edit_record, name='edit_record'),
    path('<str:table_name>/<int:first_key>/<int:second_key>/edit/', views.edit_record, name='edit_record'),
    path('<str:table_name>/<int:first_key>/delete/', views.delete_record, name='delete_record'),
    path('<str:table_name>/<int:first_key>/<int:second_key>/delete/', views.delete_record, name='delete_record'),
    path('<str:table_name>/add/', views.add_record, name='add_record'),
    path('count_attacks/<int:character_id>/', views.count_attacks, name='count_attacks'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)