def get_user_role(user):
    if user.is_superuser:
        return 'admin'
    if hasattr(user, 'teacher'):
        return 'teacher'
    if hasattr(user, 'student'):
        return 'student'
    return 'unknown'

