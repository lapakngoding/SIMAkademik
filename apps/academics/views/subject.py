from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.accounts.mixins import RoleRequiredMixin
from ..models import MataPelajaran

class SubjectListView(RoleRequiredMixin, ListView):
    model = MataPelajaran
    template_name = 'dashboard/academics/matapelajaran/subject_list.html'
    context_object_name = 'subjects'

class SubjectCreateView(RoleRequiredMixin, CreateView):
    model = MataPelajaran
    fields = ['nama', 'kode', 'pengampu']
    template_name = 'dashboard/academics/matapelajaran/subject_form.html'
    success_url = reverse_lazy('academics:subject_list')

class SubjectUpdateView(RoleRequiredMixin, UpdateView):
    model = MataPelajaran
    fields = ['nama', 'kode', 'pengampu']
    template_name = 'dashboard/academics/matapelajaran/subject_form.html'
    success_url = reverse_lazy('academics:subject_list')

class SubjectDeleteView(RoleRequiredMixin, DeleteView):
    model = MataPelajaran
    template_name = 'dashboard/academics/matapelajaran/subject_confirm_delete.html'
    success_url = reverse_lazy('academics:subject_list')
