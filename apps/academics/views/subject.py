from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.accounts.mixins import RoleRequiredMixin
from ..models import Subject
from django.contrib import messages

class SubjectListView(RoleRequiredMixin, ListView):
    model = Subject
    template_name = 'dashboard/academics/matapelajaran/subject_list.html'
    context_object_name = 'subjects'
    # Tentukan siapa yang boleh melihat list
    allowed_roles = ['admin', 'teacher'] 

class SubjectCreateView(RoleRequiredMixin, CreateView):
    model = Subject
    fields = ['nama', 'kode', 'pengampu']
    template_name = 'dashboard/academics/matapelajaran/subject_form.html'
    success_url = reverse_lazy('academics:subject_list')
    allowed_roles = ['admin'] # Biasanya cuma admin yang boleh tambah mapel

    def form_valid(self, form):
        messages.success(self.request, "Mata Pelajaran berhasil ditambahkan!")
        return super().form_valid(form)

class SubjectUpdateView(RoleRequiredMixin, UpdateView):
    model = Subject
    fields = ['nama', 'kode', 'pengampu']
    template_name = 'dashboard/academics/matapelajaran/subject_form.html'
    success_url = reverse_lazy('academics:subject_list')
    allowed_roles = ['admin']

    def form_valid(self, form):
        messages.success(self.request, "Mata Pelajaran berhasil diperbarui!")
        return super().form_valid(form)

class SubjectDeleteView(RoleRequiredMixin, DeleteView):
    model = Subject
    template_name = 'dashboard/academics/matapelajaran/subject_confirm_delete.html'
    success_url = reverse_lazy('academics:subject_list')
    allowed_roles = ['admin']

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Mata Pelajaran berhasil dihapus!")
        return super().delete(request, *args, **kwargs)
