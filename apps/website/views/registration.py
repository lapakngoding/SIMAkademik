# apps/website/views/registration.py

from django.shortcuts import render, redirect, get_object_or_404
from apps.students.models import Registration  # Pastikan path model benar
from apps.accounts.models import UserProfile, StudentProfile
from apps.website.models import SchoolProfile
from ..forms import RegistrationForm

def registration_create(request):
    school_info = SchoolProfile.objects.first()

    if request.method == 'POST':
        # Ambil semua data dari POST
        form = RegistrationForm(request.POST, request.FILES)
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

        if form.is_valid():
            registration = form.save()
            # Redirect ke halaman sukses sambil membawa ID-nya
            return redirect('website:registration_success', registration_id=registration.id)
    else:
        form = RegistrationForm()

    return render(request, 'website/ppdb.html',{
        'school': school_info,
    
    })


def registration_success(request, registration_id):
    reg = get_object_or_404(Registration, id=registration_id)
    return render(request, 'website/registration_success.html', {'reg': reg})

def print_registration_card(request, registration_id):
    # Ambil data pendaftaran berdasarkan ID
    registration = get_object_or_404(Registration, id=registration_id)
    
    context = {
        'reg': registration,
        'title': 'Kartu Bukti Pendaftaran',
    }
    return render(request, 'website/registration_card.html', context)
