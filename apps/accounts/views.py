#apps/accounts/views.py
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash # Penting agar tidak logout pas ganti password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .utils import get_user_role
from .forms import UserForm, BaseProfileForm, TeacherProfileForm, StudentProfileForm
from .models import User, UserProfile, TeacherProfile, StudentProfile
from apps.website.models import SchoolProfile
from .decorators import admin_only

class RoleBasedLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return '/dashboard/'

@login_required
def lock_screen(request):
    request.session['is_locked'] = True
    return render(request, 'registration/lock_screen.html')

@login_required
def unlock_screen(request):
    if request.method == 'POST':
        password = request.POST.get('password')

        user = authenticate(
            username=request.user.username,
            password=password
        )

        if user:
            request.session['is_locked'] = False
            return redirect('dashboard')

        messages.error(request, 'Password salah')

    return redirect('accounts:lock_screen')

# apps/accounts/views.py
@login_required
def profile_view(request):
    school_info = SchoolProfile.objects.first()
    user = request.user
    # Ambil Profile Dasar
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    # Ambil Detail Spesifik
    teacher_detail = None
    student_detail = None
    if user.role == 'teacher':
        teacher_detail, _ = TeacherProfile.objects.get_or_create(user_profile=profile)
        detail_instance = teacher_detail
        FormClass = TeacherProfileForm
    elif user.role == 'student':
        student_detail, _ = StudentProfile.objects.get_or_create(user_profile=profile)
        detail_instance = student_detail
        FormClass = StudentProfileForm
    else:
        detail_instance = None
        FormClass = None

    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=user)
        # PENTING: Tambahkan request.FILES di base_form
        base_form = BaseProfileForm(request.POST, request.FILES, instance=profile)
        
        profile_form = None
        if FormClass:
            profile_form = FormClass(request.POST, request.FILES, instance=detail_instance)

        # Cek Validasi
        is_sub_valid = profile_form.is_valid() if profile_form else True

        if u_form.is_valid() and base_form.is_valid() and is_sub_valid:
            # SAVE USER DENGAN PROTEKSI PASSWORD
            user_obj = u_form.save(commit=False)
            password = u_form.cleaned_data.get('password')
            if password: 
                user_obj.set_password(password)
            user_obj.save()
            
            # Update session supaya TIDAK LOGOUT
            update_session_auth_hash(request, user_obj)

            # SAVE PROFILE (Tempat lahir, tgl lahir, dll)
            base_form.save()

            # SAVE DETAIL (Foto, NIP/NISN)
            if profile_form:
                profile_form.save()

            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('accounts:profile')
        else:
            print(u_form.errors, base_form.errors) # Cek error di terminal
            messages.error(request, 'Gagal simpan. Periksa kembali data Anda.')
    
    else:
        # GET REQUEST
        u_form = UserForm(instance=user)
        u_form.fields['password'].initial = ""
        base_form = BaseProfileForm(instance=profile)
        profile_form = FormClass(instance=detail_instance) if FormClass else None

    return render(request, 'accounts/profile.html', {
        'u_form': u_form,
        'base_form': base_form,
        'profile_form': profile_form,
        'profile': profile,
        'school': school_info,
        'teacher_detail': teacher_detail, # Pastikan ini dikirim
        'student_detail': student_detail, # Pastikan ini dikirim
    })

# LIST GURU
@admin_only
def teacher_list(request):
    teachers = User.objects.filter(role='teacher')
    return render(request, 'accounts/teacher_list.html', {'teachers': teachers})

# TAMBAH GURU
@admin_only
def teacher_create(request):
    u_form = UserForm()
    p_form = BaseProfileForm()
    t_form = TeacherProfileForm()

    if request.method == 'POST':
        u_form = UserForm(request.POST)
        p_form = BaseProfileForm(request.POST)
        t_form = TeacherProfileForm(request.POST)
        
        if u_form.is_valid() and p_form.is_valid() and t_form.is_valid():
            # 1. Simpan User
            user = u_form.save(commit=False)
            user.set_password(u_form.cleaned_data.get('password'))
            user.role = 'teacher'
            user.is_active = True  # PASTIKAN AKTIF
            user.is_staff = True   # Beri akses staff agar bisa masuk ke beberapa view admin jika perlu
            user.save()
            
            # 2. Ambil Profile yang dibuat otomatis oleh Signal
            profile = user.userprofile
            teacher_detail = profile.teacher_detail
            
            # 3. Update Profile Utama (Nama, NIK, dll)
            p_form = BaseProfileForm(request.POST, request.FILES, instance=profile)
            if p_form.is_valid():
                p_form.save()
            
            # 4. Update Detail Guru (NIP, Status, dll)
            t_form = TeacherProfileForm(request.POST, instance=teacher_detail)
            if t_form.is_valid():
                t_form.save()
            
            messages.success(request, f'Guru {user.username} berhasil didaftarkan!')
            return redirect('accounts:teacher_list')
        else:
            messages.error(request, 'Terjadi kesalahan. Silakan periksa kembali form Anda.')

    context = {
        'u_form': u_form,
        'p_form': p_form,
        't_form': t_form,
        'title': 'Tambah Guru'
    }
    return render(request, 'accounts/teacher_form.html', context)

@admin_only
def teacher_edit(request, pk):
    teacher = get_object_or_404(User, pk=pk)
    profile = teacher.userprofile
    # Ambil detail, jika tidak ada (None), form akan menganggap ini data baru
    detail = TeacherProfile.objects.filter(user_profile=profile).first()

    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=teacher)
        p_form = BaseProfileForm(request.POST, instance=profile)
        t_form = TeacherProfileForm(request.POST, instance=detail)
        
        if u_form.is_valid() and p_form.is_valid() and t_form.is_valid():
            # 1. Simpan User
            user = u_form.save(commit=False)
            new_password = u_form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)
            user.save()
            
            # 2. Simpan Profile Utama
            p_form.save()
            
            # 3. Simpan Teacher Detail (LOGIKA PENYELAMAT)
            teacher_detail = t_form.save(commit=False)
            if not detail:
                # Jika data TeacherProfile belum ada di DB, hubungkan ke profile sekarang
                teacher_detail.user_profile = profile
            teacher_detail.save()
            
            messages.success(request, 'Data guru berhasil diupdate!')
            return redirect('accounts:teacher_list')
    else:
        u_form = UserForm(instance=teacher)
        u_form.fields['password'].initial = ""
        p_form = BaseProfileForm(instance=profile)
        t_form = TeacherProfileForm(instance=detail)

    return render(request, 'accounts/teacher_form.html', {
        'u_form': u_form, 'p_form': p_form, 't_form': t_form, 'title': 'Edit Guru'
    })

# DELETE GURU
@admin_only
def teacher_delete(request, pk):
    teacher = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Guru berhasil dihapus!')
        return redirect('accounts:teacher_list')
    return render(request, 'accounts/teacher_confirm_delete.html', {'teacher': teacher})

# LIST SISWA
@admin_only
def student_list(request):
    students = User.objects.filter(role='student')
    return render(request, 'accounts/student_list.html', {'students': students})

@admin_only
def student_create(request):
    u_form = UserForm()
    p_form = BaseProfileForm()
    s_form = StudentProfileForm()

    if request.method == 'POST':
        u_form = UserForm(request.POST)
        p_form = BaseProfileForm(request.POST)
        s_form = StudentProfileForm(request.POST)
        
        if u_form.is_valid() and p_form.is_valid() and s_form.is_valid():
            user = u_form.save(commit=False)
            user.set_password(u_form.cleaned_data.get('password'))
            user.role = 'student'
            user.is_active = True
            user.save()
            
            # Update Profile (Signal otomatis buat UserProfile & StudentProfile)
            profile = user.userprofile
            student_detail = getattr(profile, 'student_detail', None)
            
            if not student_detail:
                student_detail = StudentProfile.objects.create(user_profile=profile)
            
            p_form = BaseProfileForm(request.POST, request.FILES, instance=profile)
            s_form = StudentProfileForm(request.POST, instance=student_detail)
            
            if p_form.is_valid() and s_form.is_valid():
                p_form.save()
                s_form.save()
                messages.success(request, f'Siswa {user.username} berhasil ditambah!')
                return redirect('accounts:student_list')

    return render(request, 'accounts/student_form.html', {
        'u_form': u_form, 'p_form': p_form, 's_form': s_form, 'title': 'Tambah Siswa'
    })

@admin_only
def student_edit(request, pk):
    student = get_object_or_404(User, pk=pk)
    profile = student.userprofile
    
    # Ambil detail. Jika tidak ada, biarkan None dulu (jangan get_or_create)
    detail = StudentProfile.objects.filter(user_profile=profile).first()

    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=student)
        p_form = BaseProfileForm(request.POST, instance=profile)
        s_form = StudentProfileForm(request.POST, instance=detail)
        
        if u_form.is_valid() and p_form.is_valid() and s_form.is_valid():
            # 1. Simpan User
            user = u_form.save(commit=False)
            new_password = u_form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)
            user.save()
            
            # 2. Simpan Profile Utama
            p_form.save()
            
            # 3. Simpan Student Detail (Logika penyelamat)
            student_detail = s_form.save(commit=False)
            if not detail:
                # Jika tadi detailnya None (belum ada di DB), hubungkan ke profile sekarang
                student_detail.user_profile = profile
            student_detail.save()
            
            messages.success(request, 'Data siswa berhasil diperbarui!')
            return redirect('accounts:student_list')
    else:
        u_form = UserForm(instance=student)
        u_form.fields['password'].initial = ""
        p_form = BaseProfileForm(instance=profile)
        s_form = StudentProfileForm(instance=detail)

    return render(request, 'accounts/student_form.html', {
        'u_form': u_form, 'p_form': p_form, 's_form': s_form, 'title': 'Edit Siswa'
    })

@admin_only
def student_delete(request, pk):
    # Cari User-nya langsung (karena pk yang dikirim biasanya ID User)
    user_to_delete = User.objects.filter(pk=pk, role='student').first()
    
    if not user_to_delete:
        messages.error(request, f"Data siswa dengan ID {pk} tidak ditemukan.")
        return redirect('accounts:student_list')

    if request.method == 'POST':
        try:
            # Hapus User-nya, maka UserProfile & StudentProfile otomatis terhapus (Cascade)
            nama = user_to_delete.username
            user_to_delete.delete() 
            messages.success(request, f"Akun dan profil siswa {nama} berhasil dihapus.")
        except Exception as e:
            messages.error(request, f"Gagal menghapus: {str(e)}")
            
    return redirect('accounts:student_list')

