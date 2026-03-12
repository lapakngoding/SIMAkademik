from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class RoleRequiredMixin(LoginRequiredMixin): # Kita warisi LoginRequiredMixin biar aman
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        # 1. Cek apakah sudah login (sudah dihandle LoginRequiredMixin sebenarnya)
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user = request.user

        # 2. Superuser selalu tembus
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # 3. Cek berdasarkan field 'role' yang ada di model User kita
        if user.role in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)

        # 4. Kalau nggak punya akses, lempar ke dashboard atau 403
        return redirect('dashboard')
