from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Student
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/submit-exam/', views.submit_exam, name='submit_exam'),
    path('student/submission-history/', views.submission_history, name='submission_history'),
    path('student/exam-schedule/', views.exam_schedule, name='exam_schedule'),
    path('student/announcements/', views.announcements, name='announcements'),
    path('student/change-password/', views.change_password, name='change_password'),

    # Faculty
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),

    # Admin
    path('admin-portal/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
