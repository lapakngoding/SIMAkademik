# students/models.py
from django.db import models

class Student(models.Model):
    student_number = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=100)
    classroom = models.ForeignKey(
        'academics.Classroom',
        on_delete=models.SET_NULL,
        null=True
    )
    status = models.CharField(max_length=20, default='active')

