from django import template
register = template.Library()

@register.inclusion_tag('accounts/partials/user_info.html')
def user_profile_info(user):
    profile = None
    if user.is_authenticated:
        if hasattr(user, 'userprofile'):
            profile = user.userprofile
        elif hasattr(user, 'student_profile'):
            profile = user.student_profile
            
    return {
        'user': user,
        'profile': profile,
    }

@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


# 🔥 TAMBAHAN INI
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
