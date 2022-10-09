from django import forms
from students.models import Classroom
from datetime import datetime


class ClassroomModelForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = (
            'group',
        )

class ProjectsModelForm(forms.Form):
    name = forms.CharField(max_length=10)
    deadline = forms.DateTimeField(initial=datetime.now(),
        widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))

