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

