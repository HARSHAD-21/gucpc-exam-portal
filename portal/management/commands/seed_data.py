from django.core.management.base import BaseCommand
from portal.models import Student, Faculty, AdminUser, Exam, Department, Announcement
from django.utils import timezone
from datetime import date, timedelta, time


class Command(BaseCommand):
    help = 'Seed the database with initial sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Department
        dept, _ = Department.objects.get_or_create(name='IMS & Cyber Security', code='IMS-CS')

        # Admin
        if not AdminUser.objects.filter(username='admin').exists():
            a = AdminUser(username='admin', full_name='Administrator', email='admin@gucpc.edu')
            a.set_password('admin@123')
            a.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Admin: admin / admin@123'))

        # Faculty
        if not Faculty.objects.filter(faculty_id='FAC001').exists():
            f = Faculty(faculty_id='FAC001', full_name='Dr. Rakesh Patel', email='rpatel@gucpc.edu', department=dept)
            f.set_password('faculty@123')
            f.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Faculty: FAC001 / faculty@123'))
        
        faculty = Faculty.objects.get(faculty_id='FAC001')

        # Student – matches the screenshot exactly
        if not Student.objects.filter(enrollment_number='202318100124').exists():
            s = Student(
                enrollment_number='202318100124',
                full_name='PATEL NAIYA MAHESHBHAI',
                email='patelnaiya413@gmail.com',
                course='Integrated M.Sc. IT IMS & Cyber Security',
                semester=6,
                department=dept,
            )
            s.set_password('naiya@123')
            s.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Student: 202318100124 / naiya@123'))

        # Additional sample student
        if not Student.objects.filter(enrollment_number='202318100125').exists():
            s2 = Student(
                enrollment_number='202318100125',
                full_name='SHAH PRIYA HITESHBHAI',
                email='priyashah@gmail.com',
                course='Integrated M.Sc. IT IMS & Cyber Security',
                semester=6,
                department=dept,
            )
            s2.set_password('priya@123')
            s2.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Student: 202318100125 / priya@123'))

        # Exams
        today = date.today()
        exams_data = [
            {
                'title': 'Introduction of Cloud Computing',
                'subject_name': 'Introduction to Cloud Computing',
                'subject_code': 'DSC-M-IMS-364P',
                'exam_type': 'internal',
                'semester': 6,
                'exam_date': today - timedelta(days=9),
                'is_active': True,
                'created_by': faculty,
            },
            {
                'title': 'Internal Project Management & Planning',
                'subject_name': 'Project Management & Planning',
                'subject_code': 'DSC-C-IMS-361P',
                'exam_type': 'assignment',
                'semester': 6,
                'exam_date': today - timedelta(days=16),
                'is_active': True,
                'created_by': faculty,
            },
            {
                'title': 'Cyber Security Fundamentals',
                'subject_name': 'Cyber Security',
                'subject_code': 'DSC-M-IMS-355P',
                'exam_type': 'internal',
                'semester': 6,
                'exam_date': today + timedelta(days=5),
                'start_time': time(10, 0),
                'end_time': time(12, 0),
                'is_active': True,
                'created_by': faculty,
            },
            {
                'title': 'Network Security Practical',
                'subject_name': 'Network Security',
                'subject_code': 'DSC-M-IMS-356P',
                'exam_type': 'practical',
                'semester': 6,
                'exam_date': today + timedelta(days=12),
                'start_time': time(14, 0),
                'end_time': time(16, 0),
                'is_active': True,
                'created_by': faculty,
            },
        ]

        for ed in exams_data:
            Exam.objects.get_or_create(subject_code=ed['subject_code'], semester=ed['semester'], defaults=ed)

        self.stdout.write(self.style.SUCCESS('  ✓ Exams seeded'))

        # Announcement
        if not Announcement.objects.exists():
            admin = AdminUser.objects.first()
            Announcement.objects.create(
                title='End Semester Exam Guidelines',
                content='All students must submit their internal exam papers before the deadline. '
                        'Late submissions will not be accepted. Please ensure your files are in '
                        'PDF format. For any queries, contact the examination cell.',
                target_audience='students',
                semester=6,
                created_by=admin,
            )
            Announcement.objects.create(
                title='College Holiday Notice',
                content='The college will remain closed on account of Ambedkar Jayanti on April 14th. '
                        'All pending submissions must be completed before the holiday.',
                target_audience='all',
                created_by=admin,
            )
            self.stdout.write(self.style.SUCCESS('  ✓ Announcements seeded'))

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!\n'))
        self.stdout.write('Login credentials:')
        self.stdout.write('  Student  : 202318100124 / naiya@123')
        self.stdout.write('  Student  : 202318100125 / priya@123')
        self.stdout.write('  Faculty  : FAC001 / faculty@123')
        self.stdout.write('  Admin    : admin / admin@123')
