#apps/accounts/urls.py
from django.urls import path
from .views import lock_screen, unlock_screen, profile_view
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('lock/', lock_screen, name='lock_screen'),
    path('unlock/', unlock_screen, name='unlock_screen'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_create, name='teacher_create'),
    path('teachers/edit/<int:pk>/', views.teacher_edit, name='teacher_edit'),
    path('teachers/delete/<int:pk>/', views.teacher_delete, name='teacher_delete'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/edit/<int:pk>/', views.student_edit, name='student_edit'),
    #path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),
]
