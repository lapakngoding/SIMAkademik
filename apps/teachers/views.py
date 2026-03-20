# apps/teachers/views.py
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView
from apps.accounts.models import User
from .models import TeacherProfile
from .forms import TeacherProfileForm, TeacherCreateForm
from apps.accounts.forms import UserForm
from apps.accounts.mixins import RoleRequiredMixin
from apps.academics.models import Classroom

class TeacherCreateView(RoleRequiredMixin, CreateView):
    model = TeacherProfile
    form_class = TeacherCreateForm
    template_name = 'dashboard/teachers/teacher_form.html'
    success_url = reverse_lazy('teachers:teacher_list') # Balik ke daftar siswa
    required_role = ['admin', 'operator']

    def form_valid(self, form):
        messages.success(self.request, "Data Guru berhasil ditambahkan!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Waduh, ada yang salah input tuh. Cek lagi ya!")
        print("DEBUG FORM ERRORS:", form.errors)
        return super().form_invalid(form)

class TeacherUpdateView(SuccessMessageMixin, RoleRequiredMixin, UpdateView):
    model = TeacherProfile
    form_class = TeacherCreateForm # Gunakan form yang sama dengan Create
    template_name = 'dashboard/teachers/teacher_form.html' # Pakai template yang sama (reusable)
    success_url = reverse_lazy('teachers:teacher_list')
    required_role = ['admin', 'operator']
    success_message = "Data guru %(nama_lengkap)s berhasil diperbarui!"

    def get_object(self, queryset=None):
        # Mengambil data berdasarkan User ID agar sesuai dengan URL accounts:student_edit
        return TeacherProfile.objects.get(user_id=self.kwargs['pk'])

class TeacherListView(RoleRequiredMixin, ListView):
    model = TeacherProfile
    template_name = 'dashboard/teachers/teacher_list.html'
    context_object_name = 'teachers'
    required_role = ['admin', 'operator']

    def get_queryset(self):
        # HANYA panggil yang ada. Jika 'user' belum ada di model Student, hapus 'user'
        # Cukup gunakan select_related('classroom') jika itu satu-satunya relasi
        return TeacherProfile.objects.select_related('user','classroom').all()

@login_required
def profile_view(request):
    # 1. Proteksi Role: Hanya student yang boleh masuk sini
    if request.user.role != 'teacher':
        messages.error(request, 'Akses ditolak. Anda bukan guru.')
        return redirect('dashboard')

    # 2. Ambil data profil student
    # Gunakan related_name 'student_profile' sesuai model baru
    profile, _ = TeacherProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # u_form untuk Akun (Username/Password)
        u_form = UserForm(request.POST, instance=request.user)
        # p_form untuk Profil Siswa (Nama, Foto, Lahir, dll)
        p_form = TeacherProfileForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            # Proses Simpan User & Password
            user_obj = u_form.save(commit=False)
            password = u_form.cleaned_data.get('password')
            if password:
                user_obj.set_password(password)
            user_obj.save()
            
            # Update session supaya tidak logout otomatis
            update_session_auth_hash(request, user_obj)
            
            # Simpan data profil siswa
            p_form.save()
            
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('teachers:profile')
        else:
            messages.error(request, 'Gagal memperbarui profil. Silakan cek kembali.')
    else:
        # Tampilan awal (GET)
        u_form = UserForm(instance=request.user)
        u_form.fields['password'].initial = "" # Kosongkan field password di UI
        p_form = TeacherProfileForm(instance=profile)

    return render(request, 'dashboard/teachers/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile, # Kirim objek profile untuk preview foto
    })

@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Guru berhasil dihapus!')
        return redirect('teachers:teacher_list')
    return render(request, 'teachers/teacher_confirm_delete.html', {'teacher': teacher})

