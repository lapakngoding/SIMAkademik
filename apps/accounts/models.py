# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=(
            ('admin', 'Admin'),
            ('teacher', 'Teacher'),
            ('student', 'Student'),
        ),
        default='student'
    )

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # ======================
    # Identitas Pribadi
    # ======================
    nama_lengkap = models.CharField(max_length=150, blank=True)
    nik = models.CharField(max_length=16, blank=True)
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    tempat_lahir = models.CharField(max_length=100, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    nama_ibu_kandung = models.CharField(max_length=150, blank=True)

    # ======================
    # Kepegawaian
    # ======================
    #nip_nuptk = models.CharField(max_length=30, blank=True)
    #jabatan = models.CharField(max_length=100, blank=True)
    #pangkat_golongan = models.CharField(max_length=50, blank=True)

    # ======================
    # Unit Kerja
    # ======================
    nama_sekolah = models.CharField(max_length=200, blank=True)
    npsn = models.CharField(max_length=20, blank=True)
    alamat_sekolah = models.TextField(blank=True)
    email_unit_kerja = models.EmailField(blank=True)

    # ======================
    # Kontak Pribadi
    # ======================
    alamat_rumah = models.TextField(blank=True)
    no_hp = models.CharField(max_length=20, blank=True)
    email_pribadi = models.EmailField(blank=True)

    # ======================
    # Pendidikan
    # ======================
    pendidikan_terakhir = models.CharField(max_length=100, blank=True)
    jurusan = models.CharField(max_length=100, blank=True)
    gelar = models.CharField(max_length=50, blank=True)

    # ======================
    # Dokumen
    # ======================
    scan_ktp = models.FileField(upload_to='documents/ktp/', blank=True, null=True)
    scan_kk = models.FileField(upload_to='documents/kk/', blank=True, null=True)
    scan_sk = models.FileField(upload_to='documents/sk/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class TeacherProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='teacher_detail')
    nip_nuptk = models.CharField(max_length=20, unique=True, null=True, blank=True)
    jabatan = models.CharField(max_length=100)
    pangkat_golongan = models.CharField(max_length=50, blank=True)
    # Atribut khusus guru lainnya...

class StudentProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='student_detail')
    nisn = models.CharField(max_length=20, unique=True)
    kelas = models.CharField(max_length=20)
    nama_ibu_kandung = models.CharField(max_length=150, blank=True)
    # Atribut khusus siswa lainnya...
