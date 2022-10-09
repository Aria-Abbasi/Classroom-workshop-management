from django.contrib import admin

from .models import Student, Classroom, Project, Announcement



class StudentAdmin(admin.ModelAdmin):

    list_display = ['first_name', 'last_name', 'student_number', 'email']
    list_display_links = ['first_name']
    list_editable = ['last_name']
    search_fields = ['first_name', 'last_name', 'email']


admin.site.register(Student, StudentAdmin)
admin.site.register(Classroom)
admin.site.register(Project)
admin.site.register(Announcement)
