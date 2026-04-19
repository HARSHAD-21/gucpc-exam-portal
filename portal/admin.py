from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import (
    Student, Faculty, AdminUser,
    Exam, Submission, Announcement, Department
)
 
 
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
 
 
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['enrollment_number', 'full_name', 'email', 'semester', 'is_active']
    search_fields = ['enrollment_number', 'full_name', 'email']
    list_filter = ['semester', 'is_active']
 
    def get_form(self, request, obj=None, **kwargs):
        from django import forms
 
        class StudentForm(forms.ModelForm):
            raw_password = forms.CharField(
                label='Password',
                widget=forms.PasswordInput,
                required=(obj is None),
                help_text='Enter plain text password. Leave blank to keep existing password.'
            )
 
            class Meta:
                model = Student
                fields = ['enrollment_number', 'full_name', 'email', 'course', 'semester', 'department', 'is_active']
 
        return StudentForm
 
    def save_model(self, request, obj, form, change):
        raw_pw = form.cleaned_data.get('raw_password')
        if raw_pw:
            obj.password = make_password(raw_pw)
        elif not obj.pk:
            obj.password = make_password('changeme@123')
        obj.save()
 
 
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['faculty_id', 'full_name', 'email', 'is_active']
    search_fields = ['faculty_id', 'full_name', 'email']
 
    def get_form(self, request, obj=None, **kwargs):
        from django import forms
 
        class FacultyForm(forms.ModelForm):
            raw_password = forms.CharField(
                label='Password',
                widget=forms.PasswordInput,
                required=(obj is None),
                help_text='Plain text password.'
            )
 
            class Meta:
                model = Faculty
                fields = ['faculty_id', 'full_name', 'email', 'department', 'is_active']
 
        return FacultyForm
 
    def save_model(self, request, obj, form, change):
        raw_pw = form.cleaned_data.get('raw_password')
        if raw_pw:
            obj.password = make_password(raw_pw)
        elif not obj.pk:
            obj.password = make_password('changeme@123')
        obj.save()
 
 
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
 
 
@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'email']
 