from django.contrib.auth.decorators import login_required
from apps.students.models import Student
from . import views


@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'operator':
        return redirect('operator_dashboard')
    elif request.user.role == 'teacher':
        return redirect('teacher_dashboard')

