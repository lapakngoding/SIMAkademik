from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Student, Registration
from apps.accounts.models import UserProfile, StudentProfile
from django.views.generic import ListView
from apps.accounts.mixins import RoleRequiredMixin
from apps.website.models import SchoolProfile
from apps.academics.models import Classroom

User = get_user_model()

@transaction.atomic
def accept_student(request, pk):
    registration = get_object_or_404(Registration, pk=pk)
    
    if registration.status == 'accepted':
        messages.warning(request, "Siswa ini sudah pernah diterima.")
        return redirect('students:registration_list')

    # 1. Buat User BARU
    # Cek dulu supaya tidak error kalau username sudah ada
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

    # 2. Update atau Buat UserProfile
    # Jika Kakak pakai Signal, profil mungkin sudah ada. 
    # Kita gunakan update_or_create agar tidak bentrok.
    user_profile, _ = UserProfile.objects.update_or_create(
        user=user,
        defaults={
            'nama_lengkap': registration.full_name,
            'nik': registration.nik,
            'jenis_kelamin': registration.gender,
            'tempat_lahir': registration.tempat_lahir,
            'tanggal_lahir': registration.birth_date,
            'nama_ibu_kandung': registration.nama_ibu_kandung,
            'no_hp': registration.phone_number,
            'alamat_rumah': registration.address
        }
    )

    # 3. Buat StudentProfile
    # Gunakan update_or_create juga demi keamanan data
    StudentProfile.objects.update_or_create(
        user_profile=user_profile,
        defaults={
            'nisn': registration.nisn,
            'nama_ibu_kandung': registration.nama_ibu_kandung,
            'foto': registration.foto,
            'ijazah': registration.ijazah
        }
    )

    # 4. Update status pendaftaran
    registration.status = 'accepted'
    registration.save()

    messages.success(request, f"Pendaftaran {registration.full_name} berhasil diterima!")
    return redirect('students:registration_list')

def registration_list(request):
    # Mengambil semua pendaftar, yang terbaru di atas
    registrations = Registration.objects.all().order_by('-id')
    
    return render(request, 'dashboard/students/registration_list.html', {
        'registrations': registrations,
        'title': 'Permohonan Pendaftaran Baru'
    })


class StudentListView(RoleRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    required_role = 'operator'

def registration_detail(request, pk):
    registration = get_object_or_404(Registration, pk=pk)
    return render(request, 'dashboard/students/registration_detail.html', {
        'reg': registration,
        'title': f'Detail Pendaftaran - {registration.full_name}'
    })


