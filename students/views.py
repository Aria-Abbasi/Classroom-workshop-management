import logging
import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from classrooms.mixins import (
    OrganisorAndLoginRequiredMixin,
    OrganisorAndLoginOrYourselfRequiredMixin,
)
from .models import Student, Classroom, Project, Announcement
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import (
    StudentModelForm,
    AssignClassroomForm,
    ProjectsModelForm,
    JustStudentProjectsModelForm,
    AnnouncementsModelForm,
)
import pytz

utc = pytz.UTC


logger = logging.getLogger(__name__)


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = StudentModelForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


class DashboardView(OrganisorAndLoginRequiredMixin, generic.TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        project_not_recivied_count = Project.objects.filter(file="").count()
        project_recivied_not_graded_count = Project.objects.exclude(
            file="",
        ).filter(grade__isnull=True).count()
        thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)

        total_in_past30 = Student.objects.filter(
            date_joined__gte=thirty_days_ago, is_staff=False
        ).count()
        context.update(
            {
                "project_recivied_not_graded_count": project_recivied_not_graded_count,
                "project_not_recivied_count": project_not_recivied_count,
                "total_in_past30": total_in_past30,
            }
        )
        return context


class StudentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "students/student_list.html"
    context_object_name = "students"

    def get_queryset(self):
        return Student.objects.filter(is_staff=False)

    def get_context_data(self, **kwargs):
        return super(StudentListView, self).get_context_data(**kwargs)


class StudentDetailView(OrganisorAndLoginOrYourselfRequiredMixin, generic.DetailView):
    template_name = "students/student_detail.html"
    context_object_name = "student"

    def get_queryset(self):
        queryset = Student.objects.filter(is_staff=False)
        return queryset


class StudentUpdateView(OrganisorAndLoginOrYourselfRequiredMixin, generic.UpdateView):
    template_name = "students/student_update.html"
    form_class = StudentModelForm

    def get_queryset(self):
        return Student.objects.filter(is_staff=False)

    def get_success_url(self):
        return reverse("students:student-list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated details")
        return super(StudentUpdateView, self).form_valid(form)


class StudentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "students/student_delete.html"

    def get_success_url(self):
        return reverse("students:student-list")

    def get_queryset(self):
        return Student.objects.filter(is_staff=False)


class ProjectCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "students/project_create.html"
    form_class = ProjectsModelForm

    def get_success_url(self):
        return reverse("students:project-list")


class ProjectListView(LoginRequiredMixin,generic.ListView):
    template_name = "students/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Project.objects.all()
        elif self.request.user.is_authenticated:
            return Project.objects.filter(student=self.request.user)

    def get_context_data(self, **kwargs):
        return super(ProjectListView, self).get_context_data(**kwargs)


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "students/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Project.objects.all()
        elif self.request.user.is_authenticated:
            return Project.objects.filter(student=self.request.user)


class ProjectDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "students/project_delete.html"

    def get_success_url(self):
        return reverse("students:project-list")

    def get_queryset(self):
        return Project.objects.all()


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "students/project_update.html"
    form_class = ProjectsModelForm

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Project.objects.all()
        elif self.request.user.is_authenticated:
            return Project.objects.filter(student=self.request.user)

    def get_form_class(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return ProjectsModelForm
        elif self.request.user.is_authenticated:
            return JustStudentProjectsModelForm

    def get_success_url(self):
        return reverse("students:project-list")

    def form_valid(self, form):
        if (
            Project.objects.get(id=self.kwargs["pk"]).deadline
            < pytz.timezone("Asia/Tehran").localize(datetime.datetime.now())
            and not self.request.user.is_staff
        ):
            messages.error(self.request, "Deadline is passed")
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.info(self.request, "You have successfully updated this project")
            return super(ProjectUpdateView, self).form_valid(form)


class AnnouncementCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "students/announcement_create.html"
    form_class = AnnouncementsModelForm

    def get_success_url(self):
        return reverse("students:announcement-list")


class AnnouncementListView(OrganisorAndLoginRequiredMixin,generic.ListView):
    template_name = "students/announcement_list.html"
    context_object_name = "announcements"

    def get_queryset(self):
        return Announcement.objects.all()


class AnnouncementDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "students/announcement_detail.html"
    context_object_name = "announcement"

    def get_queryset(self):
        return Announcement.objects.all()


class AnnouncementDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "students/student_delete.html"

    def get_success_url(self):
        return reverse("students:announcement-list")

    def get_queryset(self):
        return Announcement.objects.all()


class AnnouncementUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "students/announcement_update.html"
    form_class = AnnouncementsModelForm

    def get_queryset(self):
        return Announcement.objects.all()

    def get_success_url(self):
        return reverse("students:announcement-list")

    def form_valid(self, form):
        messages.info(self.request, "You have successfully updated this announcement")
        return super(AnnouncementUpdateView, self).form_valid(form)

