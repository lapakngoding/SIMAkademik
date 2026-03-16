from django import forms
from .models import Registration, StudentProfile

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'full_name', 'gender', 'nisn', 'nik', 'tempat_lahir', 
            'birth_date', 'email', 'phone_number', 'address', 'asal_sekolah'
        ]
        widgets = {
            # Bikin input tanggal jadi kalender
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class StudentProfileForm(forms.ModelForm): # Pastikan namanya persis ini
    class Meta:
        model = StudentProfile
        fields = ['nama_lengkap', 'nisn', 'tempat_lahir', 'tanggal_lahir', 'foto','ijazah','nik','jenis_kelamin','alamat_rumah','no_hp','email_pribadi']
