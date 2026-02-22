# attendance/models.py
from django.db import models

class Attendance(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20)

