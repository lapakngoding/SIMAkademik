from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import User, UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            # ======================
            # Identitas Pribadi
            # ======================
            'nama_lengkap',
            'nik',
            'jenis_kelamin',
            'tempat_lahir',
            'tanggal_lahir',
            'nama_ibu_kandung',

            # ======================
            # Kepegawaian
            # ======================
            'nip_nuptk',
            'jabatan',
            'pangkat_golongan',

            # ======================
            # Unit Kerja
            # ======================
            'nama_sekolah',
            'npsn',
            'alamat_sekolah',
            'email_unit_kerja',

            # ======================
            # Kontak Pribadi
            # ======================
            'alamat_rumah',
            'no_hp',
            'email_pribadi',

            # ======================
            # Pendidikan
            # ======================
            'pendidikan_terakhir',
            'jurusan',
            'gelar',

            # ======================
            # Dokumen
            # ======================
            'scan_ktp',
            'scan_kk',
            'scan_sk',
        ]

        widgets = {
            # Identitas Pribadi
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control'}),
            'nik': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_lahir': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'nama_ibu_kandung': forms.TextInput(attrs={'class': 'form-control'}),

            # Kepegawaian
            'nip_nuptk': forms.TextInput(attrs={'class': 'form-control'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control'}),
            'pangkat_golongan': forms.TextInput(attrs={'class': 'form-control'}),

            # Unit Kerja
            'nama_sekolah': forms.TextInput(attrs={'class': 'form-control'}),
            'npsn': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat_sekolah': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'email_unit_kerja': forms.EmailInput(attrs={'class': 'form-control'}),

            # Kontak Pribadi
            'alamat_rumah': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'no_hp': forms.TextInput(attrs={'class': 'form-control'}),
            'email_pribadi': forms.EmailInput(attrs={'class': 'form-control'}),

            # Pendidikan
            'pendidikan_terakhir': forms.TextInput(attrs={'class': 'form-control'}),
            'jurusan': forms.TextInput(attrs={'class': 'form-control'}),
            'gelar': forms.TextInput(attrs={'class': 'form-control'}),

            # Dokumen
            'scan_ktp': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'scan_kk': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'scan_sk': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

