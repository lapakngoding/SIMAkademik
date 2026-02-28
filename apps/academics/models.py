# apps/academics/models.py
from django.db import models
from apps.accounts.models import User # Mengacu ke Custom User Anda

class Classroom(models.Model):
    nama = models.CharField(max_length=50) # Contoh: X-IPA-1
    wali_kelas = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return self.nama

class MataPelajaran(models.Model):
    nama = models.CharField(max_length=100)
    kode = models.CharField(max_length=10, unique=True)
    pengampu = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return f"{self.kode} - {self.nama}"
