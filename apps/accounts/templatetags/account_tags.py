from django import template
register = template.Library()

@register.inclusion_tag('accounts/partials/user_info.html') # Sesuaikan template tag Suhu
def user_profile_info(user):
    profile = None
    if user.is_authenticated:
        # Cek apakah user punya userprofile (untuk Admin/Guru)
        if hasattr(user, 'userprofile'):
            profile = user.userprofile
        # C el juga apakah user punya student_profile (untuk Siswa)
        elif hasattr(user, 'student_profile'):
            profile = user.student_profile
            
    return {
        'user': user,
        'profile': profile,
    }

@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
