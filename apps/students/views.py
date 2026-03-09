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

def accept_student(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    
    if reg.status == 'pending':
        try:
            with transaction.atomic():
                # 1. BUAT/AMBIL USER (Tetap sama)
                username = reg.nisn
                password_default = reg.birth_date.strftime('%d%m%Y')
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={'email': reg.email, 'role': 'student'}
                )
                if created:
                    user.set_password(password_default)
                    user.save()

                # 2. ISI USERPROFILE (Tetap sama)
                user_profile, _ = UserProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        'nama_lengkap': reg.full_name,
                        'nik': reg.nik,
                        # ... data lainnya ...
                    }
                )
                
                # 3. AMBIL KELAS (Tetap sama)
                default_class = Classroom.objects.first()

                # 4. ISI STUDENTPROFILE (Tambahkan Foto, Ijazah, dan Ibu)
                student_prof, _ = StudentProfile.objects.update_or_create(
                    user_profile=user_profile,
                    defaults={
                        'nisn': reg.nisn,
                        'kelas': default_class,
                        'nama_ibu_kandung': reg.nama_ibu_kandung,
                        'foto': reg.foto,     # File dipindahkan
                        'ijazah': reg.ijazah, # File dipindahkan
                    }
                )

                # 5. Update status
                reg.status = 'accepted'
                reg.save()
                
                messages.success(request, f"Sukses! {reg.full_name} diterima dengan No. Reg: {reg.no_registrasi}")
        
        except Exception as e:
            messages.error(request, f"Gagal memindahkan data: {str(e)}")
            
    return redirect('students:registration_list')

def registration_create(request):
    school_info = SchoolProfile.objects.first()

    if request.method == 'POST':
        # Ambil semua data dari POST
        Registration.objects.create(
            full_name=request.POST.get('full_name'),
            gender=request.POST.get('gender'),
            nisn=request.POST.get('nisn'),
            nik=request.POST.get('nik'),
            tempat_lahir=request.POST.get('tempat_lahir'),
            birth_date=request.POST.get('birth_date'),
            email=request.POST.get('email'),
            nama_ibu_kandung=request.POST.get('nama_ibu_kandung'),
            phone_number=request.POST.get('phone_number'),
            asal_sekolah=request.POST.get('asal_sekolah'),
            foto=request.FILES.get('foto'),   # Gunakan FILES untuk file
            ijazah=request.FILES.get('ijazah'), # Gunakan FILES untuk file
            address=request.POST.get('address'),
        )

        messages.success(request, 'Alhamdulillah, data pendaftaran sudah kami terima!')
        return redirect('website:home')

    return render(request, 'website/ppdb.html',{
        'school': school_info,
    
    })

def registration_list(request):
    # Mengambil semua pendaftar, yang terbaru di atas
    registrations = Registration.objects.filter(status='pending').order_by('-registration_date')
    
    return render(request, 'dashboard/students/registration_list.html', {
        'registrations': registrations,
        'title': 'Permohonan Pendaftaran Baru'
    })


class StudentListView(RoleRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    required_role = 'operator'

