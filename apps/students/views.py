from django.views.generic import ListView
from .models import Student
from apps.accounts.mixins import RoleRequiredMixin

class StudentListView(RoleRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    required_role = 'operator'

