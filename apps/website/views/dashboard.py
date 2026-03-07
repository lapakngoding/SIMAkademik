from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import SchoolProfile
from ..forms import SchoolProfileForm

@login_required
def edit_profile(request):
    # Ambil data pertama (atau buat baru jika belum ada)
    profile, created = SchoolProfile.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        form = SchoolProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil sekolah berhasil diperbarui!")
            return redirect('website:edit_profile_sekolah')
    else:
        form = SchoolProfileForm(instance=profile)
        
    return render(request, 'dashboard/website/edit_profile.html', {'form': form})
