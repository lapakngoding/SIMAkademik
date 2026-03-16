# apps/teachers/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from apps.accounts.models import User
from .models import TeacherProfile
from .forms import TeacherProfileForm
from apps.accounts.forms import UserForm

@login_required
@teacher_only # Suhu bisa buat decorator sendiri nanti
def profile_view(request):
    profile, _ = TeacherProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # Tidak perlu UserForm lagi jika hanya ingin ganti profil
        form = TeacherProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Guru Aman!')
            return redirect('teachers:profile')
    # ... render ...
