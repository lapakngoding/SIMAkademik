# apps/academics/urls.py
from django.urls import path
from .views import classroom, subject

app_name = 'academics'

urlpatterns = [
    # Classroom URLs
    path('classrooms/', classroom.ClassroomListView.as_view(), name='classroom_list'),
    path('classrooms/add/', classroom.ClassroomCreateView.as_view(), name='classroom_create'),
    path('classrooms/edit/<int:pk>/', classroom.ClassroomUpdateView.as_view(), name='classroom_edit'),
    path('classrooms/delete/<int:pk>/', classroom.ClassroomDeleteView.as_view(), name='classroom_delete'),

    # Subject URLs
    path('subjects/', subject.SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', subject.SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/edit/<int:pk>/', subject.SubjectUpdateView.as_view(), name='subject_edit'),
    path('subjects/delete/<int:pk>/', subject.SubjectDeleteView.as_view(), name='subject_delete'),
]
