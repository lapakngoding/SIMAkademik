from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

class RoleRequiredMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if user.is_superuser and 'admin' in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)

        if hasattr(user, 'teacher') and 'teacher' in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)

        if hasattr(user, 'student') and 'student' in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)

        return redirect('/login/')

