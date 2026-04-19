# GUCPC Exam Portal – Complete Setup Guide

## 🏫 Overview
Full-stack university exam portal built with Django, replicating the UI of
`test.techcpc.in`. Students can log in, submit exam files, and view submission
history. Faculty and Admin panels are also included.

---

## 🗂️ Project Structure

```
gucpc_portal/
├── gucpc_portal/          ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portal/                ← Main app
│   ├── models.py          ← Student, Faculty, Exam, Submission, etc.
│   ├── views.py           ← All page logic
│   ├── urls.py            ← URL routes
│   ├── admin.py           ← Django admin config
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py   ← Demo data seeder
│   ├── templates/portal/  ← All HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── student_base.html
│   │   ├── student_dashboard.html
│   │   ├── submit_exam.html
│   │   ├── submission_history.html
│   │   ├── exam_schedule.html
│   │   ├── announcements.html
│   │   ├── change_password.html
│   │   ├── faculty_dashboard.html
│   │   └── admin_dashboard.html
│   └── static/portal/
│       ├── css/style.css  ← Full custom CSS (Poppins, blue-purple gradient)
│       └── js/main.js     ← Sidebar toggle, dark mode, alerts
├── media/                 ← Uploaded exam files (auto-created)
├── manage.py
├── requirements.txt
├── .env.example
├── Procfile               ← For Render/Heroku
├── render.yaml            ← Render deployment config
└── README.md
```

---

## ⚡ QUICK START (Local – Windows/Mac/Linux)

### Step 1 – Prerequisites
Make sure you have Python 3.10+ installed:
```bash
python --version
```

### Step 2 – Clone / Extract the project
```bash
# If using the zip file:
unzip gucpc_portal.zip
cd gucpc_portal

# OR if cloning from GitHub:
git clone https://github.com/YOUR_USERNAME/gucpc-portal.git
cd gucpc-portal
```

### Step 3 – Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5 – Configure environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env – at minimum change SECRET_KEY:
# SECRET_KEY=any-random-50-character-string
# DEBUG=True
# Leave DATABASE_URL blank to use SQLite locally
```

### Step 6 – Run database migrations
```bash
python manage.py migrate
```

### Step 7 – Seed demo data
```bash
python manage.py seed_data
```

This creates:
| Role    | Username/Enrollment | Password      |
|---------|---------------------|---------------|
| Student | 202318100124        | naiya@123     |
| Student | 202318100125        | priya@123     |
| Faculty | FAC001              | faculty@123   |
| Admin   | admin               | admin@123     |

### Step 8 – Start the server
```bash
python manage.py runserver
```

Open your browser: **http://127.0.0.1:8000**

---

## 📧 Email Setup (Gmail SMTP)

To send confirmation emails after exam submission:

1. Go to your Google Account → Security → 2-Step Verification → **App Passwords**
2. Generate an App Password for "Mail"
3. Add to your `.env` file:
   ```
   EMAIL_HOST_USER=youremail@gmail.com
   EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx   ← 16-char app password
   DEFAULT_FROM_EMAIL=GUCPC Exam Portal <youremail@gmail.com>
   ```

> ⚠️ Never use your actual Gmail password – always use App Passwords.

---

## 🌐 DEPLOYMENT ON RENDER (Free Hosting)

### Step 1 – Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit – GUCPC Exam Portal"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/gucpc-portal.git
git push -u origin main
```

### Step 2 – Create account on Render
Go to: https://render.com → Sign up (free)

### Step 3 – Create a PostgreSQL Database
- Dashboard → **New +** → **PostgreSQL**
- Name: `gucpc-db`
- Plan: **Free**
- Click **Create Database**
- Copy the **Internal Database URL** — you'll need it in Step 5

### Step 4 – Create a Web Service
- Dashboard → **New +** → **Web Service**
- Connect your GitHub repo
- Configure:

| Setting         | Value                                         |
|----------------|-----------------------------------------------|
| Name           | `gucpc-exam-portal`                          |
| Environment    | Python 3                                      |
| Build Command  | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| Start Command  | `gunicorn gucpc_portal.wsgi`                 |
| Plan           | Free                                          |

### Step 5 – Add Environment Variables in Render
Go to your Web Service → **Environment** tab → Add these:

| Key                  | Value                                      |
|---------------------|--------------------------------------------|
| `SECRET_KEY`         | (click "Generate" or use a random 50-char string) |
| `DEBUG`              | `False`                                    |
| `DATABASE_URL`       | (paste the Internal DB URL from Step 3)   |
| `EMAIL_HOST_USER`    | your Gmail address                         |
| `EMAIL_HOST_PASSWORD`| your Gmail App Password                   |
| `DEFAULT_FROM_EMAIL` | `GUCPC Exam Portal <youremail@gmail.com>` |

### Step 6 – Deploy & Seed Data
After deploy completes, click **Shell** tab in Render and run:
```bash
python manage.py seed_data
```

### Step 7 – Access Your Live Site
Your portal will be live at:
```
https://gucpc-exam-portal.onrender.com
```

> 💡 **Custom Domain**: Go to Render → Settings → Custom Domains → Add `test.techcpc.in`
> Then add a CNAME record in your DNS pointing to `gucpc-exam-portal.onrender.com`

---

## 🔐 Django Admin Panel

Access the built-in Django admin (for managing students, exams, etc.):

1. First create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
2. Visit: http://127.0.0.1:8000/admin/

From here you can:
- Add/edit/delete Students, Faculty, Exams
- View all submissions
- Create announcements
- Manage any data

---

## 🎨 UI Features

| Page                | Features                                                     |
|--------------------|--------------------------------------------------------------|
| **Login**          | 3 tabs (Student/Admin/Faculty), gradient header, password toggle, animated background |
| **Dashboard**      | Welcome banner, 4 stat cards, announcements, dark mode       |
| **Submit Exam**    | Student info card, guidelines box, dropdown (green=available, red=submitted), drag & drop upload |
| **History**        | Sortable table, status badges, file size, view/download link |
| **Exam Schedule**  | Table with upcoming/today/completed status badges            |
| **Announcements**  | Card layout with dates                                       |
| **Change Password**| Secure form with validation                                  |

---

## 🛠️ Adding More Students or Exams

### Via Django Admin (easiest)
1. Go to `/admin/` → Students → Add Student
2. **Important**: Hash the password using the portal's set_password method

### Via Django Shell
```bash
python manage.py shell
```
```python
from portal.models import Student
s = Student(
    enrollment_number='202318100130',
    full_name='MEHTA RAVI SURESHBHAI',
    email='ravi@gmail.com',
    course='Integrated M.Sc. IT IMS & Cyber Security',
    semester=6
)
s.set_password('ravi@123')
s.save()
```

---

## 🔧 Common Issues & Fixes

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside your venv |
| Static files 404 | Run `python manage.py collectstatic` |
| Email not sending | Check App Password, enable 2FA first in Google |
| Login fails | Run `python manage.py seed_data` to reset demo accounts |
| Render deploy fails | Check build logs, ensure all env vars are set |

---

## 📱 Responsive Design

The portal is fully responsive:
- **Desktop**: Full sidebar + main content
- **Tablet**: Collapsible sidebar
- **Mobile**: Hamburger menu, stacked cards

---

## 📄 License
Free to use for educational and personal projects.
Built for GUCPC – Ganpat University Computer Portal Centre.
