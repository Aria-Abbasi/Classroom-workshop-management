from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class OrganisorAndLoginOrYourselfRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organisor."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff and not request.user.id == self.kwargs['pk']:
            return redirect("students:student-list")
        return super().dispatch(request, *args, **kwargs)

class OrganisorAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organisor."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        elif not request.user.is_staff:
            return redirect("students:student-detail", request.user.id)
        return super().dispatch(request, *args, **kwargs)
