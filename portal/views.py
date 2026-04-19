from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
import os
import threading

from .models import Student, Faculty, AdminUser, Exam, Submission, Announcement


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_session_user(request):
    role = request.session.get('user_role')
    user_id = request.session.get('user_id')
    if not role or not user_id:
        return None, None
    try:
        if role == 'student':
            return Student.objects.get(id=user_id), role
        elif role == 'faculty':
            return Faculty.objects.get(id=user_id), role
        elif role == 'admin':
            return AdminUser.objects.get(id=user_id), role
    except Exception:
        return None, None
    return None, None


def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        user, role = get_session_user(request)
        if not user or role != 'student':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def faculty_required(view_func):
    def wrapper(request, *args, **kwargs):
        user, role = get_session_user(request)
        if not user or role != 'faculty':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        user, role = get_session_user(request)
        if not user or role != 'admin':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def send_submission_email(student, exam, submission):
    def _send():
        try:
            subject = f"Exam Submission Confirmation – {exam.title}"
            body = f"""Dear {student.full_name},

Your exam submission has been received successfully.

Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Exam          : {exam.title}
Subject       : {exam.subject_name} ({exam.subject_code})
Enrollment No : {student.enrollment_number}
Submitted At  : {submission.submitted_at.strftime('%B %d, %Y at %I:%M %p')}
File          : {submission.original_filename}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please do not reply to this email.

Regards,
GUCPC Examination Cell
test.techcpc.in
"""
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [student.email], fail_silently=True)
        except Exception:
            pass
    threading.Thread(target=_send, daemon=True).start()


# ─── Auth Views ────────────────────────────────────────────────────────────────

def login_view(request):
    if request.session.get('user_role'):
        role = request.session.get('user_role')
        if role == 'student':
            return redirect('student_dashboard')
        elif role == 'faculty':
            return redirect('faculty_dashboard')
        elif role == 'admin':
            return redirect('admin_dashboard')

    if request.method == 'POST':
        role = request.POST.get('role', 'student')
        password = request.POST.get('password', '')

        if role == 'student':
            identifier = request.POST.get('enrollment_number', '').strip()
            try:
                student = Student.objects.get(enrollment_number=identifier)
                if student.check_password(password):
                    if not student.is_active:
                        messages.error(request, 'Your account is inactive. Contact administration.')
                    else:
                        request.session['user_role'] = 'student'
                        request.session['user_id'] = student.id
                        request.session['user_name'] = student.full_name
                        return redirect('student_dashboard')
                else:
                    messages.error(request, 'Invalid enrollment number or password.')
            except Student.DoesNotExist:
                messages.error(request, 'Invalid enrollment number or password.')

        elif role == 'faculty':
            identifier = request.POST.get('faculty_id', '').strip()
            try:
                faculty = Faculty.objects.get(faculty_id=identifier)
                if faculty.check_password(password):
                    if not faculty.is_active:
                        messages.error(request, 'Your account is inactive.')
                    else:
                        request.session['user_role'] = 'faculty'
                        request.session['user_id'] = faculty.id
                        request.session['user_name'] = faculty.full_name
                        return redirect('faculty_dashboard')
                else:
                    messages.error(request, 'Invalid faculty ID or password.')
            except Faculty.DoesNotExist:
                messages.error(request, 'Invalid faculty ID or password.')

        elif role == 'admin':
            identifier = request.POST.get('username', '').strip()
            try:
                admin = AdminUser.objects.get(username=identifier)
                if admin.check_password(password):
                    request.session['user_role'] = 'admin'
                    request.session['user_id'] = admin.id
                    request.session['user_name'] = admin.full_name
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Invalid credentials.')
            except AdminUser.DoesNotExist:
                messages.error(request, 'Invalid credentials.')

    return render(request, 'portal/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


# ─── Student Views ─────────────────────────────────────────────────────────────

@student_required
def student_dashboard(request):
    student = Student.objects.get(id=request.session['user_id'])
    today = timezone.now().date()
    upcoming_exams = Exam.objects.filter(
        is_active=True, semester=student.semester, exam_date__gte=today
    ).count()
    total_submissions = Submission.objects.filter(student=student).count()
    announcements = Announcement.objects.filter(
        is_active=True,
        target_audience__in=['all', 'students']
    ).order_by('-created_at')[:5]

    # Exams not yet submitted
    submitted_exam_ids = Submission.objects.filter(student=student).values_list('exam_id', flat=True)
    available_exams_count = Exam.objects.filter(
        is_active=True, semester=student.semester
    ).exclude(id__in=submitted_exam_ids).count()

    context = {
        'student': student,
        'upcoming_exams': upcoming_exams,
        'total_submissions': total_submissions,
        'announcements': announcements,
        'available_exams_count': available_exams_count,
        'active_page': 'dashboard',
    }
    return render(request, 'portal/student_dashboard.html', context)


@student_required
def submit_exam(request):
    student = Student.objects.get(id=request.session['user_id'])
    submitted_exam_ids = list(
        Submission.objects.filter(student=student).values_list('exam_id', flat=True)
    )
    all_exams = Exam.objects.filter(is_active=True, semester=student.semester).order_by('exam_date')

    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        uploaded_file = request.FILES.get('submission_file')
        access_token_input = request.POST.get('access_token', '').strip()

        if not exam_id or not uploaded_file:
            messages.error(request, 'Please select an exam and upload a file.')
            return redirect('submit_exam')

        try:
            exam = Exam.objects.get(id=exam_id, is_active=True, semester=student.semester)
        except Exam.DoesNotExist:
            messages.error(request, 'Invalid exam selected.')
            return redirect('submit_exam')

        if int(exam_id) in submitted_exam_ids:
            messages.error(request, 'You have already submitted this exam.')
            return redirect('submit_exam')

        if exam.requires_token and exam.access_token != access_token_input:
            messages.error(request, 'Invalid access token.')
            return redirect('submit_exam')

        allowed_extensions = ['.pdf', '.doc', '.docx', '.zip', '.rar', '.jpg', '.jpeg', '.png']
        _, ext = os.path.splitext(uploaded_file.name.lower())
        if ext not in allowed_extensions:
            messages.error(request, f'File type "{ext}" is not allowed.')
            return redirect('submit_exam')

        submission = Submission.objects.create(
            student=student,
            exam=exam,
            file=uploaded_file,
            original_filename=uploaded_file.name,
            file_size=uploaded_file.size,
            status='submitted'
        )
        send_submission_email(student, exam, submission)
        messages.success(request, f'"{exam.title}" submitted successfully! A confirmation email has been sent.')
        return redirect('submission_history')

    context = {
        'student': student,
        'all_exams': all_exams,
        'submitted_exam_ids': submitted_exam_ids,
        'active_page': 'submit_exam',
    }
    return render(request, 'portal/submit_exam.html', context)


@student_required
def submission_history(request):
    student = Student.objects.get(id=request.session['user_id'])
    sort = request.GET.get('sort', 'newest')
    status_filter = request.GET.get('status', 'all')

    submissions = Submission.objects.filter(student=student).select_related('exam')

    if status_filter != 'all':
        submissions = submissions.filter(status=status_filter)

    if sort == 'oldest':
        submissions = submissions.order_by('submitted_at')
    else:
        submissions = submissions.order_by('-submitted_at')

    context = {
        'student': student,
        'submissions': submissions,
        'sort': sort,
        'status_filter': status_filter,
        'active_page': 'submission_history',
    }
    return render(request, 'portal/submission_history.html', context)


@student_required
def exam_schedule(request):
    student = Student.objects.get(id=request.session['user_id'])
    today = timezone.now().date()
    exams = Exam.objects.filter(is_active=True, semester=student.semester).order_by('exam_date')
    context = {
        'student': student,
        'exams': exams,
        'today': today,
        'active_page': 'exam_schedule',
    }
    return render(request, 'portal/exam_schedule.html', context)


@student_required
def announcements(request):
    student = Student.objects.get(id=request.session['user_id'])
    anns = Announcement.objects.filter(
        is_active=True,
        target_audience__in=['all', 'students']
    ).order_by('-created_at')
    context = {
        'student': student,
        'announcements': anns,
        'active_page': 'announcements',
    }
    return render(request, 'portal/announcements.html', context)


@student_required
def change_password(request):
    student = Student.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        current = request.POST.get('current_password', '')
        new_pw = request.POST.get('new_password', '')
        confirm = request.POST.get('confirm_password', '')
        if not student.check_password(current):
            messages.error(request, 'Current password is incorrect.')
        elif new_pw != confirm:
            messages.error(request, 'New passwords do not match.')
        elif len(new_pw) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        else:
            student.set_password(new_pw)
            student.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('student_dashboard')
    context = {'student': student, 'active_page': 'change_password'}
    return render(request, 'portal/change_password.html', context)


# ─── Faculty Views ─────────────────────────────────────────────────────────────

@faculty_required
def faculty_dashboard(request):
    faculty = Faculty.objects.get(id=request.session['user_id'])
    return render(request, 'portal/faculty_dashboard.html', {'faculty': faculty})


# ─── Admin Views ───────────────────────────────────────────────────────────────

@admin_required
def admin_dashboard(request):
    admin = AdminUser.objects.get(id=request.session['user_id'])
    total_students = Student.objects.count()
    total_submissions = Submission.objects.count()
    total_exams = Exam.objects.count()
    recent_submissions = Submission.objects.select_related('student', 'exam').order_by('-submitted_at')[:10]
    context = {
        'admin': admin,
        'total_students': total_students,
        'total_submissions': total_submissions,
        'total_exams': total_exams,
        'recent_submissions': recent_submissions,
    }
    return render(request, 'portal/admin_dashboard.html', context)
