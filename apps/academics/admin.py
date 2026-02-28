from django.contrib import admin
from .models import Classroom  # Import model yang ingin dimunculkan

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama')  # Menampilkan kolom ID dan Nama di daftar
    search_fields = ('nama',)      # Menambahkan fitur pencarian berdasarkan nama
