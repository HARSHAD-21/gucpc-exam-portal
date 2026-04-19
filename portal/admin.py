from django.contrib import admin
from .models import Student, Faculty, AdminUser, Exam, Submission, Announcement, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['enrollment_number', 'full_name', 'email', 'course', 'semester', 'is_active']
    search_fields = ['enrollment_number', 'full_name', 'email']
    list_filter = ['semester', 'is_active']


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['faculty_id', 'full_name', 'email', 'is_active']
    search_fields = ['faculty_id', 'full_name', 'email']


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'email']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject_code', 'exam_type', 'semester', 'exam_date', 'is_active']
    list_filter = ['exam_type', 'semester', 'is_active']
    search_fields = ['title', 'subject_code', 'subject_name']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'status', 'submitted_at']
    list_filter = ['status']
    search_fields = ['student__enrollment_number', 'student__full_name']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_audience', 'is_active', 'created_at']
    list_filter = ['target_audience', 'is_active']
