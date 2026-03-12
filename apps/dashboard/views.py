# apps/dahsboard/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import User 
from apps.students.models import Registration
from django.db.models import Count
from django.db.models.functions import ExtractMonth
import calendar

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

        # Profile logic yang sudah ada
        try:
            context['profile'] = user.userprofile
        except Exception:
            context['profile'] = None
        
        # Statistik untuk Admin
        if user.role == 'admin':
            context['total_guru'] = User.objects.filter(role='teacher').count()
            context['total_siswa'] = User.objects.filter(role='student').count()
            context['total_pendaftar'] = Registration.objects.count()
            context['pendaftar_pending'] = Registration.objects.filter(status='pending').count()
            context['recent_activities'] = Registration.objects.all().order_by('-registration_date')[:5]

            # Logika Grafik: Pendaftar 6 Bulan Terakhir
            monthly_data = Registration.objects.annotate(month=ExtractMonth('registration_date'))\
                                               .values('month')\
                                               .annotate(count=Count('id'))\
                                               .order_by('month')
            
            labels = []
            data = []
            for entry in monthly_data:
                labels.append(calendar.month_name[entry['month']])
                data.append(entry['count'])

            context['chart_labels'] = labels
            context['chart_data'] = data

        # Data spesifik role (logic Kakak yang lama)
        if user.role == 'teacher' and hasattr(user, 'userprofile') and hasattr(user.userprofile, 'teacher_detail'):
            context['detail'] = user.userprofile.teacher_detail
        elif user.role == 'student' and hasattr(user, 'userprofile') and hasattr(user.userprofile, 'student_detail'):
            context['detail'] = user.userprofile.student_detail
            
        return context
