# students/models.py
from django.conf import settings
import datetime
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Registration(models.Model):
    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Diterima'),
        ('rejected', 'Ditolak'),
    ]
    
    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    nisn = models.CharField(max_length=20)
    nik = models.CharField(max_length=20)
    tempat_lahir = models.CharField(max_length=25)
    birth_date = models.DateField()
    email = models.EmailField()
    no_registrasi = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    nama_ibu_kandung = models.CharField(max_length=150, blank=True, null=True)
    foto = models.ImageField(upload_to='photos/registration/', null=True, blank=True)
    ijazah = models.FileField(upload_to='documents/ijazah/', null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    asal_sekolah = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if not self.no_registrasi:
            # Ambil tanggal hari ini
            today = datetime.date.today()
            date_str = today.strftime('%Y%m%d') # Format: 20260309
            
            # Cari pendaftar terakhir di hari yang sama untuk menentukan nomor urut
            last_reg = Registration.objects.filter(no_registrasi__startswith=date_str).order_by('-no_registrasi').first()
            
            if last_reg:
                # Ambil 3 angka terakhir dan tambah 1
                last_no = int(last_reg.no_registrasi[-3:])
                new_no = str(last_no + 1).zfill(3)
            else:
                new_no = '001'
            
            self.no_registrasi = f"{date_str}{new_no}"
            
        super(Registration, self).save(*args, **kwargs)


class StudentProfile(models.Model):
    GENDER_CHOICES = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )

    
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='student_profile')
    nama_lengkap = models.CharField(max_length=255)
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    nik = models.CharField(max_length=16, blank=True)
    nisn = models.CharField(max_length=20, unique=True)
    foto = models.ImageField(upload_to='photos/students/', blank=True, null=True)
    ijazah = models.FileField(upload_to='documents/students/ijazah/', null=True, blank=True)
    tempat_lahir = models.CharField(max_length=100, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    nama_ibu_kandung = models.CharField(max_length=100, blank=True)
    alamat_rumah = models.TextField(blank=True)
    no_hp = models.CharField(max_length=20, blank=True)
    email_pribadi = models.EmailField(blank=True)
    status_akademik = models.CharField(
        max_length=20, 
        choices=[('aktif', 'Aktif'), ('lulus', 'Lulus'), ('drop', 'Putus Sekolah')],
        default='aktif'
    )
    classroom = models.ForeignKey(
        'academics.Classroom', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='students'
    )

