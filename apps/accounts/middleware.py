from django.shortcuts import redirect
from django.urls import reverse

class LockScreenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.session.get('is_locked'):
                lock_url = reverse('lock_screen')
                unlock_url = reverse('unlock_screen')

                if request.path not in [lock_url, unlock_url]:
                    return redirect('lock_screen')

        return self.get_response(request)

