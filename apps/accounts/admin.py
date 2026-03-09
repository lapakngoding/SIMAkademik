from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StudentProfile, User, UserProfile # Tambahkan UserProfile jika perlu

# 1. HAPUS baris admin.site.register(User, UserAdmin) yang lama

# 2. Definisikan CustomUserAdmin
class CustomUserAdmin(UserAdmin):
    # Menambahkan field 'role' ke tampilan edit user di admin
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role',)}),
    )
    # Menampilkan kolom role di daftar tabel user
    list_display = ['username', 'email', 'role', 'is_staff']

# 3. Daftarkan User dengan CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'kelas')
    list_filter = ('kelas',)
    list_editable = ('kelas',)

# Jika ingin UserProfile muncul juga
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'nik', 'no_hp')
