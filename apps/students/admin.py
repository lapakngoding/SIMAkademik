from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentAdmin(admin.ModelAdmin):
    # Ganti 'nisn' dengan nama fungsi yang kita buat di bawah
    list_display = ('user', 'get_nisn', 'classroom') 

    # Fungsi untuk mengambil NISN dari profile
    def get_nisn(self, obj):
        # Sesuaikan dengan cara Suhu memanggil profile (misal: user.student_profile.nisn)
        try:
            return obj.user.student_profile.nisn
        except:
            return "-"
    
    # Memberi nama kolom di tampilan Admin
    get_nisn.short_description = 'NISN'
