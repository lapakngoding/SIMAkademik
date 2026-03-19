# apps/students/views.py
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView

# Import dari aplikasi sendiri
from .models import Registration, StudentProfile
from .forms import StudentProfileForm, StudentCreateForm

# Import dari aplikasi lain
from apps.accounts.forms import UserForm
from apps.accounts.mixins import RoleRequiredMixin
#from apps.website.models import SchoolProfile
from apps.academics.models import Classroom

# Definisi User
User = get_user_model()

@transaction.atomic
def accept_student(request, pk):
    registration = get_object_or_404(Registration, pk=pk)
    
    # ... pengecekan status ...

    # 1. Buat User BARU (Login Akun)
    user, created = User.objects.get_or_create(
        username=registration.nisn,
        defaults={
            'email': registration.email,
            'role': 'student',
            'first_name': registration.full_name
        }
    )
    
    if created:
        user.set_password('password123')
        user.save()

    # 2. Langsung buat StudentProfile (Aplikasi Students)
    # Kita tidak lagi pakai UserProfile dari apps.accounts
    StudentProfile.objects.update_or_create(
        user=user, # Hubungkan langsung ke User
        defaults={
            'nama_lengkap': registration.full_name,
            'nisn': registration.nisn,
            'tempat_lahir': registration.tempat_lahir,
            'tanggal_lahir': registration.birth_date,
            'nama_ibu_kandung': registration.nama_ibu_kandung,
            'foto': registration.foto,
            'ijazah': registration.ijazah # Pastikan field ini ada di model StudentProfile
        }
    )

    # 3. Update status pendaftaran
    registration.status = 'accepted'
    registration.save()

    messages.success(request, f"Pendaftaran {registration.full_name} berhasil diterima!")
    return redirect('students:registration_list')

def registration_list(request):
    # Mengambil semua pendaftar, yang terbaru di atas
    registrations = Registration.objects.all().order_by('-id')
    
    stats = {
        'total': registrations.count(),
        'pending': registrations.filter(status='pending').count(),
        'accepted': registrations.filter(status='accepted').count(),
    }
    
    return render(request, 'dashboard/students/registration_list.html', {
        'registrations': registrations,
        'stats': stats,
        'title': 'Permohonan Pendaftaran Baru'
    })

@login_required
def profile_view(request):
    # 1. Proteksi Role: Hanya student yang boleh masuk sini
    if request.user.role != 'student':
        messages.error(request, 'Akses ditolak. Anda bukan siswa.')
        return redirect('dashboard')

    # 2. Ambil data profil student
    # Gunakan related_name 'student_profile' sesuai model baru
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # u_form untuk Akun (Username/Password)
        u_form = UserForm(request.POST, instance=request.user)
        # p_form untuk Profil Siswa (Nama, Foto, Lahir, dll)
        p_form = StudentProfileForm(request.POST, request.FILES, instance=profile)

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
            return redirect('students:profile')
        else:
            messages.error(request, 'Gagal memperbarui profil. Silakan cek kembali.')
    else:
        # Tampilan awal (GET)
        u_form = UserForm(instance=request.user)
        u_form.fields['password'].initial = "" # Kosongkan field password di UI
        p_form = StudentProfileForm(instance=profile)

    return render(request, 'students/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile, # Kirim objek profile untuk preview foto
    })

@login_required
def student_profile_update(request):
    user = request.user
    student_detail, _ = StudentProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=user)
        p_form = StudentProfileForm(request.POST, request.FILES, instance=student_detail)

        if u_form.is_valid() and p_form.is_valid():
            user_obj = u_form.save(commit=False)
            
            # Ambil password dari input manual
            new_password = u_form.cleaned_data.get('password')
            
            if new_password and new_password.strip():
                # User beneran ngetik password baru
                user_obj.set_password(new_password)
                user_obj.save()
                update_session_auth_hash(request, user_obj)
            else:
                # USER TIDAK ISI PASSWORD:
                # Ambil password (hash) yang sudah ada di DB agar tidak tertimpa
                user_obj.password = User.objects.get(pk=user.pk).password
                user_obj.save()

            p_form.save()
            messages.success(request, 'Profil berhasil diupdate!')
            return redirect('students:profile')
    else:
        u_form = UserForm(instance=user)
        p_form = StudentProfileForm(instance=student_detail)

    return render(request, 'students/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
    })

class StudentListView(RoleRequiredMixin, ListView):
    model = StudentProfile
    template_name = 'dashboard/students/student_list.html'
    context_object_name = 'students'
    required_role = 'admin'

    def get_queryset(self):
        # HANYA panggil yang ada. Jika 'user' belum ada di model Student, hapus 'user'
        # Cukup gunakan select_related('classroom') jika itu satu-satunya relasi
        return StudentProfile.objects.select_related('user','classroom').all()

def registration_detail(request, pk):
    registration = get_object_or_404(Registration, pk=pk)
    return render(request, 'dashboard/students/registration_detail.html', {
        'reg': registration,
        'title': f'Detail Pendaftaran - {registration.full_name}'
    })

class StudentCreateView(RoleRequiredMixin, CreateView):
    model = StudentProfile
    form_class = StudentCreateForm
    template_name = 'dashboard/students/student_form.html'
    success_url = reverse_lazy('students:student_list') # Balik ke daftar siswa
    required_role = ['admin', 'operator']

    def form_valid(self, form):
        messages.success(self.request, "Data siswa berhasil ditambahkan!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Waduh, ada yang salah input tuh. Cek lagi ya!")
        print("DEBUG FORM ERRORS:", form.errors)
        return super().form_invalid(form)

class StudentUpdateView(SuccessMessageMixin, RoleRequiredMixin, UpdateView):
    model = StudentProfile
    form_class = StudentCreateForm # Gunakan form yang sama dengan Create
    template_name = 'dashboard/students/student_form.html' # Pakai template yang sama (reusable)
    success_url = reverse_lazy('students:student_list')
    required_role = 'admin'
    success_message = "Data siswa %(nama_lengkap)s berhasil diperbarui!"

    def get_object(self, queryset=None):
        # Mengambil data berdasarkan User ID agar sesuai dengan URL accounts:student_edit
        return StudentProfile.objects.get(user_id=self.kwargs['pk'])



