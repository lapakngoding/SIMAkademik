#apps/academics/views/classroom.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.accounts.mixins import RoleRequiredMixin
from ..models import Classroom

class ClassroomListView(RoleRequiredMixin, ListView):
    model = Classroom
    template_name = 'dashboard/academics/classroom/classroom_list.html'
    context_object_name = 'classrooms'

class ClassroomCreateView(RoleRequiredMixin, CreateView):
    model = Classroom
    fields = ['nama', 'wali_kelas']
    template_name = 'dashboard/academics/classroom/classroom_form.html'
    success_url = reverse_lazy('academics:classroom_list')

class ClassroomUpdateView(RoleRequiredMixin, UpdateView):
    model = Classroom
    fields = ['nama', 'wali_kelas']
    template_name = 'dashboard/academics/classroom/classroom_form.html'
    success_url = reverse_lazy('academics:classroom_list')

class ClassroomDeleteView(RoleRequiredMixin, DeleteView):
    model = Classroom
    template_name = 'dashboard/academics/classroom/classroom_confirm_delete.html'
    success_url = reverse_lazy('academics:classroom_list')
