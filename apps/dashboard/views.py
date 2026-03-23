# apps/dahsboard/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import User 
from apps.students.models import Registration
from django.db.models import Count
from django.db.models.functions import ExtractMonth
import calendar
from django.utils import timezone
from apps.academics.models import Schedule

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

            # 1. Logika Ambil Profil yang Universal
            if user.role == 'student':
                # Untuk siswa, ambil dari StudentProfile
                profile = getattr(user, 'student_profile', None)
            else:
                # Untuk admin/teacher, ambil dari UserProfile
                profile = getattr(user, 'userprofile', None)
            
            context['profile'] = profile

            # 2. Statistik untuk Admin (Tetap sama)
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

            # 3. Logika Detail Spesifik Role (Perbaikan di sini)
            if user.role == 'student' and profile:
                # Kita buatkan variabel 'detail' agar template Suhu tidak error
                context['detail'] = {
                    'nisn': profile.nisn,
                    'kelas': profile.classroom.name if profile.classroom else "Belum Ada Kelas",
                }

                today_en = timezone.localtime().strftime('%A')

                day_map = {
                    'Monday': 'Senin',
                    'Tuesday': 'Selasa',
                    'Wednesday': 'Rabu',
                    'Thursday': 'Kamis',
                    'Friday': 'Jumat',
                    'Saturday': 'Sabtu',
                    'Sunday': 'Minggu'
                }

                today = day_map.get(today_en)

                schedules = Schedule.objects.filter(
                    classroom=profile.classroom,
                    day__iexact=today
                )
                
                context['schedules'] = schedules

            elif user.role == 'teacher' and profile:
                context['detail'] = getattr(profile, 'teacher_detail', None)
                
            return context
