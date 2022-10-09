
from django.urls import path
from .views import (
    StudentListView, StudentDetailView, StudentUpdateView, StudentDeleteView,
    ProjectListView, ProjectDetailView, ProjectUpdateView, ProjectDeleteView, ProjectCreateView,
    AnnouncementListView, AnnouncementDetailView, AnnouncementUpdateView, AnnouncementDeleteView, AnnouncementCreateView,
)
app_name = "students"

urlpatterns = [
    path('', StudentListView.as_view(), name='student-list'),
    path('grades/', ProjectListView.as_view(), name='project-list'),
    path('announcement/', AnnouncementListView.as_view(), name='announcement-list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('grades/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('announcement/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student-update'),
    path('grades/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('announcement/<int:pk>/update/', AnnouncementUpdateView.as_view(), name='announcement-update'),
    # path('<int:pk>/grades/', StudentUpdateGradesView, name='student-grades'),
    path('<int:pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
    path('grades/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('announcement/<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='announcement-delete'),
    # path('create/', StudentCreateView.as_view(), name='student-create'),
    path('grades/create/', ProjectCreateView.as_view(), name='project-create'),
    path('announcement/create/', AnnouncementCreateView.as_view(), name='announcement-create'),
]