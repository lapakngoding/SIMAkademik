# teachers/models.py
from django.db import models

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
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='teacher_profile')
    nama_lengkap = models.CharField(max_length=255)
    nip_nuptk = models.CharField(max_length=50, blank=True)
    foto = models.ImageField(upload_to='photos/teachers/', blank=True, null=True)
    tempat_lahir = models.CharField(max_length=100, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    alamat = models.TextField(blank=True)

