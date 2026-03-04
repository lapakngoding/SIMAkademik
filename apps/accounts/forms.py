# apps/accounts/forms.py
from django import forms
from django.utils import timezone
# Sesuaikan dengan model baru Anda
from .models import User, UserProfile, TeacherProfile, StudentProfile, Post

# Form untuk user auth (Username, Email, dsb)
class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Masukkan password'}),
        required=False,
        help_text="Gunakan password yang kuat."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {field: forms.TextInput(attrs={'class': 'form-control'}) for field in fields}

# Form untuk data yang ADA di SEMUA orang
class BaseProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nama_lengkap', 'tempat_lahir', 'nama_ibu_kandung', 'no_hp','nik', 'jenis_kelamin', 'tanggal_lahir', 'alamat_rumah','no_hp','email_pribadi']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 1. Semua field otomatis dapat class form-control
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        # 2. Spesifikasikan field yang butuh widget khusus
        self.fields['jenis_kelamin'].widget.attrs.update(
            attrs={'class': 'form-control'}
        )
        self.fields['tanggal_lahir'].widget = forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        )
        self.fields['alamat_rumah'].widget = forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3}
        )
        

# Form khusus GURU
class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile # Model baru yang kita rencanakan
        fields = ['nip_nuptk', 'jabatan', 'pangkat_golongan']
        widgets = {field: forms.TextInput(attrs={'class': 'form-control'}) for field in fields}

# Form khusus SISWA
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile # Model baru yang kita rencanakan
        fields = ['nisn', 'kelas','nama_ibu_kandung']
        widgets = {field: forms.TextInput(attrs={'class': 'form-control'}) for field in fields}


from django_ckeditor_5.widgets import CKEditor5Widget

# apps/website/forms.py

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        
        # Pastikan format initial value-nya benar-benar bersih (hanya Tahun-Bulan-HariTJam:Menit)
        if not self.instance.pk:
            self.initial['published_at'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
        else:
            # Jika sedang EDIT, pastikan data lama diformat ulang agar bisa dibaca input HTML5
            if self.instance.published_at:
                self.initial['published_at'] = self.instance.published_at.strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Post
        fields = ['title', 'content', 'published_at']
        widgets = {
            'published_at': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'step': '60', # Ini kuncinya! '60' artinya kelipatan 60 detik (1 menit).
                },
                format='%Y-%m-%dT%H:%M'
            ),
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, 
                config_name="extends"
            )
        }
