from django import forms
from .models import TeacherProfile, User

class TeacherProfileForm(forms.ModelForm): # Pastikan namanya persis ini
    class Meta:
        model = TeacherProfile
        fields = ['nama_lengkap', 'nip_nuptk', 'nama_ibu_kandung', 'tempat_lahir', 'tanggal_lahir', 'foto','ijazah','nik','jenis_kelamin','alamat_rumah','no_hp','email_pribadi']

class TeacherCreateForm(forms.ModelForm):
    # Field tambahan dari model User
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=False)

    class Meta:
        model = TeacherProfile
        fields = ['nama_lengkap', 'nip_nuptk', 'tempat_lahir', 'tanggal_lahir','nama_ibu_kandung', 'foto','ijazah','nik','jenis_kelamin','alamat_rumah','no_hp','email_pribadi','classroom','status']
        widgets = {
            'tanggal_lahir': forms.DateInput(
                attrs={
                    'type': 'date', # Ini kunci biar muncul kalender
                    'class': 'form-control',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(TeacherCreateForm, self).__init__(*args, **kwargs)
        
        # PERBAIKAN DI SINI:
        # Cek apakah instance sudah punya ID (berarti sedang EDIT)
        # dan cek apakah objek user-nya benar-benar ada
        if self.instance.pk and hasattr(self.instance, 'user') and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            # Saat edit, password tidak wajib diisi
            self.fields['password'].required = False
            self.fields['password'].help_text = "Kosongkan jika tidak ingin mengganti password"
        else:
            # Saat TAMBAH BARU, password wajib diisi
            self.fields['password'].required = True

    def clean_username(self):
        username = self.cleaned_data.get('username')
        nip_nuptk = self.cleaned_data.get('nip_nuptk')

        # Jika username kosong, kita isi pakai NIP NUPTK
        if not username:
            if not nip_nuptk:
                raise forms.ValidationError("Username kosong, minimal isi NIP NUPTK untuk username otomatis.")
            username = nip_nuptk
        
        # Cek duplikat (seperti biasa)
        user_exists = User.objects.filter(username=username)
        if self.instance.pk:
            user_exists = user_exists.exclude(pk=self.instance.user.pk)
            
        if user_exists.exists():
            raise forms.ValidationError(f"Username {username} sudah ada, BosQ!")
            
        return username

    def save(self, commit=True):
        if self.instance.pk:
            # --- LOGIKA EDIT (Tetap Sama) ---
            profile = super().save(commit=False)
            user = self.instance.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            password = self.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
        else:
            # --- LOGIKA TAMBAH BARU ---
            # 1. Buat User (Ini akan memicu Signal)
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                role='teacher'
            )
            
            # 2. Ambil profil yang OTOMATIS dibuat oleh Signal tadi
            # Pastikan nama field di get() sesuai dengan model Suhu
            profile, created = TeacherProfile.objects.get_or_create(user=user)
            
            # 3. Masukkan data dari Form ke profil tersebut
            # Kita gunakan cara manual agar data form menimpa profil kosong dari signal
            for field in self.cleaned_data:
                if field not in ['username', 'password', 'email']:
                    setattr(profile, field, self.cleaned_data[field])

        if commit:
            profile.save()
        return profile
