# apps/academics/models/subject.py
from django.db import models
from apps.accounts.models import User

#MataPelajaran
class Subject(models.Model):
    nama = models.CharField(max_length=100)
    kode = models.CharField(max_length=10, unique=True)
    pengampu = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return f"{self.kode} - {self.nama}"
