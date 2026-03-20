#apps/teachers/urls.py
from django.urls import path
from .views import TeacherListView, TeacherCreateView, TeacherUpdateView
from . import views

app_name = 'teachers'

urlpatterns = [

    path('teacher/', TeacherListView.as_view(), name='teacher_list'),
    path('add/teacher', TeacherCreateView.as_view(), name='teacher_create'),
    path('profile/', views.profile_view, name='profile'),
    path('teachers/<int:pk>/edit/', views.TeacherUpdateView.as_view(), name='teacher_edit'),
    path('teachers/delete/<int:pk>/', views.teacher_delete, name='teacher_delete'),

]

