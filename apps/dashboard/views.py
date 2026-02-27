# apps/dashboard/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        role = self.request.user.role
        mapping = {
            'admin': 'admin/dashboard.html',
            'teacher': 'dashboard/teachers/teacher.html',
            'student': 'dashboard/students/student.html',
        }
        return [mapping.get(role, 'dashboard/default.html')]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Mengambil data dasar
        context['profile'] = user.userprofile
        
        # Mengambil data spesifik berdasarkan role
        if user.role == 'teacher' and hasattr(user.userprofile, 'teacher_detail'):
            context['detail'] = user.userprofile.teacher_detail
        elif user.role == 'student' and hasattr(user.userprofile, 'student_detail'):
            context['detail'] = user.userprofile.student_detail
            
        return context
