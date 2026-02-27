from django import template
register = template.Library()

@register.inclusion_tag('accounts/partials/user_info.html', takes_context=True)
def user_profile_info(context):
    request = context['request']
    user = request.user
    
    # Return data untuk template partial
    return {
        'profile': user.userprofile if user.is_authenticated else None,
        'user': user
    }
