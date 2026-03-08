from django import forms
from .models import Registration

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
