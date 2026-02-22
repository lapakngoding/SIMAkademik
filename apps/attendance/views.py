from django.contrib.auth.decorators import login_required
from students.models import Student

@login_required
def attendance_input(request):
    # hanya siswa dari kelas guru
    students = Student.objects.filter(
        classroom__teacher=request.user.teacher
    )

