# apps/accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile, TeacherProfile, StudentProfile # Perhatikan nama kelasnya

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # 1. Buat UserProfile (Data Dasar)
        profile = UserProfile.objects.get_or_create(user=instance)[0]
        
        # 2. Buat Detail Spesifik
        if instance.role == 'teacher':
            TeacherProfile.objects.get_or_create(user_profile=profile)
        elif instance.role == 'student':
            StudentProfile.objects.get_or_create(user_profile=profile)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Hanya lakukan jika diperlukan, dan hindari .save() rekursif
    try:
        profile = instance.userprofile
        # Tidak perlu .save() di sini, cukup biarkan model mengurus dirinya sendiri
    except UserProfile.DoesNotExist:
        pass
