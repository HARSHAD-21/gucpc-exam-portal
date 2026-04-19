from django.core.management.base import BaseCommand
from portal.models import Student, Faculty, AdminUser, Exam, Department, Announcement
from django.contrib.auth.models import User
from datetime import date, timedelta, time
 
 
class Command(BaseCommand):
    help = 'Seed the database with initial sample data'
 
    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
 
        # Department
        dept, _ = Department.objects.get_or_create(
            name='IMS & Cyber Security', code='IMS-CS'
        )
 
        # Django Superuser (for /admin/ panel)
        if not User.objects.filter(username='superadmin').exists():
            User.objects.create_superuser(
                username='superadmin',
                email='superadmin@gucpc.edu',
                password='SuperAdmin@123'
            )
            self.stdout.write(self.style.SUCCESS(
                '  ✓ Django Superuser: superadmin / SuperAdmin@123'
            ))
 
        # Portal Admin
        if not AdminUser.objects.filter(username='admin').exists():
            a = AdminUser(username='admin', full_name='Administrator', email='admin@gucpc.edu')
            a.set_password('admin@123')
            a.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Portal Admin: admin / admin@123'))
 
        # Faculty
        if not Faculty.objects.filter(faculty_id='FAC001').exists():
            f = Faculty(faculty_id='FAC001', full_name='Dr. Rakesh Patel', email='rpatel@gucpc.edu', department=dept)
            f.set_password('faculty@123')
            f.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Faculty: FAC001 / faculty@123'))
 
        faculty = Faculty.objects.get(faculty_id='FAC001')
 
        # Students
        students_data = [
            {'enrollment_number': '202318100124', 'full_name': 'PATEL NAIYA MAHESHBHAI', 'email': 'patelnaiya413@gmail.com', 'password': 'naiya@123', 'semester': 6},
            {'enrollment_number': '202318100125', 'full_name': 'SHAH PRIYA HITESHBHAI', 'email': 'priyashah@gmail.com', 'password': 'priya@123', 'semester': 6},
            {'enrollment_number': '202318100126', 'full_name': 'MEHTA RAVI SURESHBHAI', 'email': 'ravimehta@gmail.com', 'password': 'ravi@123', 'semester': 6},
        ]
 
        for sd in students_data:
            if not Student.objects.filter(enrollment_number=sd['enrollment_number']).exists():
                s = Student(
                    enrollment_number=sd['enrollment_number'],
                    full_name=sd['full_name'],
                    email=sd['email'],
                    course='Integrated M.Sc. IT IMS & Cyber Security',
                    semester=sd['semester'],
                    department=dept,
                )
                s.set_password(sd['password'])
                s.save()
                self.stdout.write(self.style.SUCCESS(f"  ✓ Student: {sd['enrollment_number']} / {sd['password']}"))
 
        # Exams
        today = date.today()
        exams_data = [
            {'title': 'Introduction of Cloud Computing', 'subject_name': 'Introduction to Cloud Computing', 'subject_code': 'DSC-M-IMS-364P', 'exam_type': 'internal', 'semester': 6, 'exam_date': today - timedelta(days=9), 'is_active': True, 'created_by': faculty},
            {'title': 'Internal Project Management & Planning', 'subject_name': 'Project Management & Planning', 'subject_code': 'DSC-C-IMS-361P', 'exam_type': 'assignment', 'semester': 6, 'exam_date': today - timedelta(days=16), 'is_active': True, 'created_by': faculty},
            {'title': 'Cyber Security Fundamentals', 'subject_name': 'Cyber Security', 'subject_code': 'DSC-M-IMS-355P', 'exam_type': 'internal', 'semester': 6, 'exam_date': today + timedelta(days=5), 'start_time': time(10, 0), 'end_time': time(12, 0), 'is_active': True, 'created_by': faculty},
            {'title': 'Network Security Practical', 'subject_name': 'Network Security', 'subject_code': 'DSC-M-IMS-356P', 'exam_type': 'practical', 'semester': 6, 'exam_date': today + timedelta(days=12), 'start_time': time(14, 0), 'end_time': time(16, 0), 'is_active': True, 'created_by': faculty},
        ]
 
        for ed in exams_data:
            Exam.objects.get_or_create(subject_code=ed['subject_code'], semester=ed['semester'], defaults=ed)
 
        self.stdout.write(self.style.SUCCESS('  ✓ Exams seeded'))
 
        # Announcements
        if not Announcement.objects.exists():
            admin = AdminUser.objects.first()
            Announcement.objects.create(title='End Semester Exam Guidelines', content='All students must submit their internal exam papers before the deadline. Late submissions will not be accepted. Please ensure your files are in PDF format. For any queries, contact the examination cell.', target_audience='students', semester=6, created_by=admin)
            Announcement.objects.create(title='College Holiday Notice', content='The college will remain closed on account of Ambedkar Jayanti on April 14th. All pending submissions must be completed before the holiday.', target_audience='all', created_by=admin)
            self.stdout.write(self.style.SUCCESS('  ✓ Announcements seeded'))
 
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!\n'))
        self.stdout.write('=' * 45)
        self.stdout.write('LOGIN CREDENTIALS:')
        self.stdout.write('=' * 45)
        self.stdout.write('STUDENTS:')
        self.stdout.write('  202318100124  /  naiya@123')
        self.stdout.write('  202318100125  /  priya@123')
        self.stdout.write('  202318100126  /  ravi@123')
        self.stdout.write('FACULTY:  FAC001 / faculty@123')
        self.stdout.write('PORTAL ADMIN:  admin / admin@123')
        self.stdout.write('DJANGO ADMIN (/admin/):  superadmin / SuperAdmin@123')
        self.stdout.write('=' * 45)
 