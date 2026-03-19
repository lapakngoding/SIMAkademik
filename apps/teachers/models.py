# teachers/models.py
from django.conf import settings
import datetime
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Teacher(models.Model):
    employee_number = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=100)
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

class TeacherProfile(models.Model):
    GENDER_CHOICES = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )    

    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='teacher_profile')
    nama_lengkap = models.CharField(max_length=255)
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    nik = models.CharField(max_length=16, blank=True)
    nip_nuptk = models.CharField(max_length=50, blank=True)
    foto = models.ImageField(upload_to='photos/teachers/', blank=True, null=True)
    ijazah = models.FileField(upload_to='documents/teachers/ijazah/', null=True, blank=True)
    nama_ibu_kandung = models.CharField(max_length=100, blank=True)
    tempat_lahir = models.CharField(max_length=100, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    no_hp = models.CharField(max_length=20, blank=True)
    email_pribadi = models.EmailField(blank=True)
    alamat_rumah = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=[('aktif', 'Aktif'), ('pindah', 'Pindah'), ('resign', 'Mengundurkan diri')],
        default='aktif'
    )
    classroom = models.ForeignKey(
        'academics.Classroom', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='teachers'
    )

