from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .utils import get_user_role

class RoleBasedLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        role = get_user_role(self.request.user)

        if role == 'admin':
            return '/dashboard/'
        elif role == 'teacher':
            return '/dashboard/teacher/'
        elif role == 'student':
            return '/dashboard/student/'
        return '/login/'

@login_required
def lock_screen(request):
    request.session['is_locked'] = True
    return render(request, 'registration/lock_screen.html')

@login_required
def unlock_screen(request):
    if request.method == 'POST':
        password = request.POST.get('password')

        user = authenticate(
            username=request.user.username,
            password=password
        )

        if user:
            request.session['is_locked'] = False
            return redirect('dashboard')

        messages.error(request, 'Password salah')

    return redirect('lock_screen')
