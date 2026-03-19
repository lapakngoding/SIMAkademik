# apps/students/forms.py
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
        fields = ['nama_lengkap', 'nisn', 'nama_ibu_kandung', 'tempat_lahir', 'tanggal_lahir', 'foto','ijazah','nik','jenis_kelamin','alamat_rumah','no_hp','email_pribadi']

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

    def __init__(self, *args, **kwargs):
        super(StudentCreateForm, self).__init__(*args, **kwargs)
        
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
        nisn = self.cleaned_data.get('nisn')

        # Jika username kosong, kita isi pakai NISN
        if not username:
            if not nisn:
                raise forms.ValidationError("Username kosong, minimal isi NISN untuk username otomatis.")
            username = nisn
        
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
                role='student'
            )
            
            # 2. Ambil profil yang OTOMATIS dibuat oleh Signal tadi
            # Pastikan nama field di get() sesuai dengan model Suhu
            profile, created = StudentProfile.objects.get_or_create(user=user)
            
            # 3. Masukkan data dari Form ke profil tersebut
            # Kita gunakan cara manual agar data form menimpa profil kosong dari signal
            for field in self.cleaned_data:
                if field not in ['username', 'password', 'email']:
                    setattr(profile, field, self.cleaned_data[field])

        if commit:
            profile.save()
        return profile
