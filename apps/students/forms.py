from django import forms
from .models import Registration, StudentProfile, User

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

class StudentCreateForm(forms.ModelForm):
    # Field tambahan dari model User
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=False)

    class Meta:
        model = StudentProfile
        fields = ['nama_lengkap', 'nisn', 'tempat_lahir', 'tanggal_lahir','nama_ibu_kandung', 'foto','ijazah','nik','jenis_kelamin','alamat_rumah','no_hp','email_pribadi','classroom','status_akademik']
        widgets = {
            'tanggal_lahir': forms.DateInput(
                attrs={
                    'type': 'date', # Ini kunci biar muncul kalender
                    'class': 'form-control',
                }
            ),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username ini sudah digunakan, cari yang lain ya BosQ.")
        return username

    def save(self, commit=True):
        # 1. Simpan User dulu
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            role='student' # Otomatis set role student
        )
        # 2. Simpan Profile
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile
