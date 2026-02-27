from django.contrib.auth.decorators import user_passes_test

def admin_only(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.role == 'admin',
        login_url='login' # atau arahkan ke halaman '403 Forbidden'
    )(view_func)
