import random

from django.core.mail import send_mail
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from students.models import Classroom, Project, Student
from .forms import ClassroomModelForm, ProjectsModelForm
from .mixins import OrganisorAndLoginRequiredMixin
from django.shortcuts import render
from django.template import RequestContext


class ClassroomListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "classrooms/classroom_list.html"
    context_object_name = "classrooms"
    
    def get_queryset(self):
        return Classroom.objects.all()


class ClassroomCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "classrooms/classroom_create.html"
    form_class = ClassroomModelForm

    def get_success_url(self):
        return reverse("classrooms:classroom-list")

    def form_valid(self, form):
        form.save(commit=False)
        return super(ClassroomCreateView, self).form_valid(form)



class ClassroomDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "classrooms/classroom_detail.html"
    context_object_name = "classroom"

    def get_queryset(self):
        return Classroom.objects.all()
    
    def get_context_data(self, **kwargs):
    
        context = super().get_context_data(**kwargs)
        
        context['students'] = Student.objects.filter(classroom = self.kwargs.get(self.pk_url_kwarg))
        return context


class ClassroomUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "classrooms/classroom_update.html"
    form_class = ClassroomModelForm

    def get_success_url(self):
        return reverse("classrooms:classroom-list")

    def get_queryset(self):
        return Classroom.objects.all()


class ClassroomDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "classrooms/classroom_delete.html"
    context_object_name = "classroom"

    def get_success_url(self):
        return reverse("classrooms:classroom-list")

    def get_queryset(self):
        return Classroom.objects.all()

def ProjectCreateView(request, pk):
    if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('students:project-list')
    template_name = "students/project_create.html"
    if request.method == 'POST':
        form = ProjectsModelForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            deadline = form.cleaned_data["deadline"]
            students = Student.objects.filter(classroom__id = pk)
            for student in students:
                Project.objects.create(student=student,name=name,deadline=deadline)
            classroom = Classroom.objects.get(id = pk)
            classroom.projects[f"{name}"] = name
            classroom.save()
            return redirect('students:project-list')
    else:
        form = ProjectsModelForm()

    return render(request, template_name , {'form': form})
