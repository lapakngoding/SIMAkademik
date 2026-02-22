from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.mixins import RoleRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/dashboard.html'
    login_url = '/login/'

class TeacherDashboardView(
    LoginRequiredMixin,
    RoleRequiredMixin,
    TemplateView
):
    template_name = 'dashboard/teacher.html'
    allowed_roles = ['teacher']
