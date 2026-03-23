# apps/academics/models/classroom.py
from django.db import models
from apps.accounts.models import User # Mengacu ke Custom User Anda

class Classroom(models.Model):
    name = models.CharField(max_length=50)  # contoh: 6A
    level = models.CharField(max_length=10) # contoh: SD / SMP
    academic_year = models.CharField(max_length=20) # contoh: 2025/2026

    def __str__(self):
        return f"{self.name} - {self.academic_year}"
