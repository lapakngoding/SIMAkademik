from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .utils import get_user_role
from .forms import UserForm, BaseProfileForm, TeacherProfileForm, StudentProfileForm
from .models import User, UserProfile, TeacherProfile, StudentProfile
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

    return redirect('lock_screen')

def profile_view(request):
    user = request.user
    # Pastikan user sudah login
    if not user.is_authenticated:
        return redirect('login')

    # Ambil atau buat profil
    profile, created = UserProfile.objects.get_or_create(user=user)

    # 1. DEFINISIKAN VARIABEL SEBELUM BLOK IF/ELSE
    base_form = BaseProfileForm(instance=profile)

    if request.method == 'POST':
        # 2. Re-inisialisasi form dengan data POST
        base_form = BaseProfileForm(request.POST, request.FILES, instance=profile)
        
        if base_form.is_valid():
            base_form.save()
            print("LOG: Data tersimpan")
            return redirect('accounts:profile')
        else:
            print("LOG: Form error:", base_form.errors)

    # 3. Sekarang base_form selalu ada, tidak akan error lagi
    return render(request, 'accounts/profile.html', {
        'base_form': base_form
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

# EDIT GURU
@admin_only
def teacher_edit(request, pk):
    teacher = get_object_or_404(User, pk=pk)
    profile = teacher.userprofile
    detail = TeacherProfile.objects.filter(user_profile=profile).first()

    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=teacher)
        p_form = BaseProfileForm(request.POST, instance=profile)
        t_form = TeacherProfileForm(request.POST, instance=detail)
        
        if u_form.is_valid() and p_form.is_valid() and t_form.is_valid():
            user = u_form.save(commit=False)
            
            # CEK: Apakah admin mengisi kotak password?
            new_password = u_form.cleaned_data.get('password')
            if new_password:
                # Jika diisi, enkripsi password baru
                user.set_password(new_password)
            else:
                # Jika kosong, jangan ubah password! 
                # Kita ambil password yang sudah ada di database (yang masih terenkripsi)
                user.password = User.objects.get(pk=teacher.pk).password
            
            user.save()
            p_form.save()
            t_form.save()
            
            messages.success(request, 'Data guru berhasil diupdate!')
            return redirect('accounts:teacher_list')
    else:
        # Saat GET, kita kosongkan field password di form agar tidak menampilkan hash-nya
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
