from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import StudentProfile

User = get_user_model()

admin.site.register(User, UserAdmin)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'kelas')
    list_filter = ('kelas',)
    list_editable = ('kelas',)
