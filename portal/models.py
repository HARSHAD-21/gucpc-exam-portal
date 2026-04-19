from django.db import models
from django.contrib.auth.hashers import make_password, check_password as django_check_password
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Student(models.Model):
    enrollment_number = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    course = models.CharField(max_length=200, default='Integrated M.Sc. IT IMS & Cyber Security')
    semester = models.IntegerField(default=1)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)

    @property
    def account_status(self):
        return 'Active' if self.is_active else 'Inactive'

    def __str__(self):
        return f"{self.enrollment_number} - {self.full_name}"


class Faculty(models.Model):
    faculty_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.faculty_id} - {self.full_name}"


class AdminUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)

    def __str__(self):
        return self.full_name


class Exam(models.Model):
    EXAM_TYPES = [
        ('internal', 'Internal Exam'),
        ('external', 'External Exam'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('practical', 'Practical'),
    ]
    title = models.CharField(max_length=300)
    subject_name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=50)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default='internal')
    semester = models.IntegerField(default=1)
    course = models.CharField(max_length=200, blank=True)
    exam_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    submission_deadline = models.DateTimeField(null=True, blank=True)
    access_token = models.CharField(max_length=100, blank=True)
    requires_token = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.subject_code})"

    @property
    def is_upcoming(self):
        return self.exam_date >= timezone.now().date()


class Submission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('rejected', 'Rejected'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'exam')

    def __str__(self):
        return f"{self.student.enrollment_number} - {self.exam.title}"

    @property
    def file_size_display(self):
        size = self.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size / (1024 * 1024):.2f} MB"


class Announcement(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    target_audience = models.CharField(
        max_length=20,
        choices=[('all', 'All'), ('students', 'Students'), ('faculty', 'Faculty')],
        default='all'
    )
    semester = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
