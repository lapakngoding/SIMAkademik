# grades/models.py
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)

class Grade(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

