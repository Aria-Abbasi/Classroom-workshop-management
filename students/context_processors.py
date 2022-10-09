from .models import Announcement
from django.db.models import Q

def announcement_context_processor(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return {"announcements": Announcement.objects.filter(Q(classroom__isnull=True) | Q(classroom = request.user.classroom), display=True)}
    elif request.user.is_authenticated and request.user.is_staff:
        return {"announcements": Announcement.objects.filter(display=True)}
    else:
        return {"announcements": None}