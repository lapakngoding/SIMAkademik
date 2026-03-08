# students/models.py
from django.db import models

class Registration(models.Model):
    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Diterima'),
        ('rejected', 'Ditolak'),
    ]
    
    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=20)
    nisn = models.CharField(max_length=20)
    nik = models.CharField(max_length=20)
    tempat_lahir = models.CharField(max_length=25)
    birth_date = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    asal_sekolah = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.full_name

class Student(models.Model):
    student_number = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=100)
    classroom = models.ForeignKey(
        'academics.Classroom',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.CharField(max_length=20, default='active')

