from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Student, Classroom, Project, Announcement
from django.contrib.admin import widgets

User = get_user_model()


class StudentModelForm(UserCreationForm):
    class Meta:
        model = Student
        fields = (
            "username",
            "first_name",
            "last_name",
            "student_number",
            "classroom",
            "phone_number",
            "email",
            "profile_picture",
        )
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classroom'].required = True


class AssignClassroomForm(forms.Form):
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        classrooms = Classroom.objects.all()
        super(AssignClassroomForm, self).__init__(*args, **kwargs)
        self.fields["classroom"].queryset = classrooms


class ProjectsModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "name",
            "student",
            "grade",
            "deadline",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["deadline"].widget = forms.widgets.DateTimeInput(
            attrs={"type": "datetime-local"}
        )
        self.fields["student"].queryset = Student.objects.filter(is_staff=False)


class JustStudentProjectsModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("file",)


class AnnouncementsModelForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = (
            "level",
            "classroom",
            "display",
            "body",
        )