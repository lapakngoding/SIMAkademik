from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class RoleRequiredMixin(LoginRequiredMixin):
    # Kita buat defaultnya kosong
    required_role = None 

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user = request.user

        # Superuser sakti, selalu boleh lewat
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Cek apakah role user ada di dalam required_role yang diset di View
        # Kita handle kalau required_role itu string tunggal atau list
        role_akses = self.required_role
        if isinstance(role_akses, str):
            role_akses = [role_akses] # Ubah jadi list kalau cuma satu string

        if user.role in role_akses:
            return super().dispatch(request, *args, **kwargs)

        # Kalau gagal, lempar ke dashboard
        return redirect('dashboard')
