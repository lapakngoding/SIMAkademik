# academics/models.py
from django.db import models

class AcademicYear(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)

class Classroom(models.Model):
    name = models.CharField(max_length=50)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

