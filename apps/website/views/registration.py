# apps/website/views/registration.py

from django.shortcuts import render, redirect, get_object_or_404
from apps.students.models import Registration  # Pastikan path model benar
from apps.accounts.models import UserProfile, StudentProfile
from apps.website.models import SchoolProfile
from ..forms import RegistrationForm

def registration_create(request):
    school_info = SchoolProfile.objects.first()

    if request.method == 'POST':
        # Gunakan Form, jangan simpan manual lewat objects.create jika ingin validasi
        form = RegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Simpan data secara otomatis
            registration = form.save()
            # Redirect menggunakan id dari data yang baru disimpan
            return redirect('website:registration_success', registration_id=registration.id)
    else:
        # Jika GET (buka halaman pertama kali)
        form = RegistrationForm()

    return render(request, 'website/ppdb.html', {
        'school': school_info,
        'form': form, # Kirim variabel form ke template
        'title': 'Pendaftaran Siswa Baru',
    })


def registration_success(request, registration_id):
    school_info = SchoolProfile.objects.first()
    reg = get_object_or_404(Registration, id=registration_id)
    return render(request, 'website/registration_success.html', {'school': school_info,'reg': reg})

def print_registration_card(request, registration_id):
    school_info = SchoolProfile.objects.first()
    # Ambil data pendaftaran berdasarkan ID
    registration = get_object_or_404(Registration, id=registration_id)
    
    context = {
        'school': school_info,
        'reg': registration,
        'title': 'Kartu Bukti Pendaftaran',
    }
    return render(request, 'website/registration_card.html', context)
