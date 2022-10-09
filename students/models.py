from django.db import models
from django.contrib.auth.models import AbstractUser


class Student(AbstractUser):
    student_number = models.IntegerField(default=0)
    classroom = models.ForeignKey(
        "Classroom", null=True, blank=True, on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to="profile_pictures/"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Classroom(models.Model):
    group = models.IntegerField(unique=True)
    projects = models.JSONField(default=dict)

    def __str__(self):
        return str(self.group)


class Project(models.Model):
    name = models.CharField(max_length=20)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    grade = models.FloatField(null=True, blank=True)
    deadline = models.DateTimeField()
    file = models.FileField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    LEVEL_CHOICES = (
        ("warning", "Warning"),
        ("error", "Error"),
        ("success", "Success"),
        ("info", "Info"),
    )
    body = models.TextField(blank=False)
    classroom = models.ForeignKey(
        "Classroom", null=True, blank=True, on_delete=models.CASCADE
    )
    display = models.BooleanField(default=False)
    level = models.CharField(max_length=7, choices=LEVEL_CHOICES, default="info")
