# Submitly

> A web-based assignment submission and evaluation platform built with Django.

Submitly is a role-based academic platform designed to simplify the complete assignment lifecycle between faculty and students.

Faculty can create courses, publish assignments, attach reference materials, review submissions, assign marks, and provide feedback. Students can enroll in courses, view assignments, submit their work, and track evaluation results from a single dashboard.

---

## ✨ Features

### 👨‍🎓 Student

- Student account registration
- Role-based authentication
- Student dashboard
- Browse available courses
- Request course enrollment
- View approved courses
- View published assignments
- View assignment instructions and due dates
- Download assignment reference materials
- Submit assignments
- Upload supported document formats
- Track submission status
- View marks and faculty feedback
- View personal profile

### 👨‍🏫 Faculty

- Faculty authentication
- Faculty dashboard
- Create and manage courses
- Review student enrollment requests
- Approve or reject enrollment requests
- Create assignments
- Set assignment descriptions and due dates
- Set maximum marks
- Publish assignments
- Attach reference materials
- View student submissions
- Review submitted work
- Assign marks
- Provide feedback
- Track assignment submissions
- View faculty profile

### 🔐 Authentication & Authorization

- Custom Django user model
- Email-based authentication
- Student and Faculty roles
- Role-based dashboard redirection
- Role-based access control
- Protected faculty/student routes
- Secure logout
- Student registration
- Profile page

### 📎 File Management

Students can submit:

- PDF
- DOC
- DOCX
- PPT
- PPTX
- TXT

Faculty can attach reference materials using the same supported formats.

File uploads are limited to **10 MB**.

### 🎨 UI/UX

- Submitly branding
- Consistent navigation
- Student and faculty-specific dashboards
- Responsive layout
- Modern card-based interface
- Consistent action buttons
- Assignment and submission status indicators
- Profile navigation
- Clean authentication pages
- Presentation-ready interface

---

## 🔄 Assignment Workflow

Submitly follows a simple academic workflow:

```text
Faculty
   │
   ├── Create Course
   │
   ├── Review Enrollment Requests
   │       ├── Approve
   │       └── Reject
   │
   ├── Create Assignment
   │
   ├── Attach Reference Material
   │
   └── Publish Assignment
            │
            ▼
         Student
            │
            ├── View Assignment
            │
            ├── Read Instructions
            │
            ├── Download Reference
            │
            └── Submit Work
                    │
                    ▼
                  Faculty
                    │
                    ├── Review Submission
                    ├── Assign Marks
                    └── Provide Feedback
                            │
                            ▼
                          Student
                            │
                            └── View Result & Feedback
```

---

## 🛠️ Tech Stack

### Backend

- **Python**
- **Django 5.2**
- **Django ORM**
- **Gunicorn**

### Frontend

- **Django Templates**
- **HTML5**
- **CSS3**
- **JavaScript**

### Database

- **PostgreSQL**
- **SQLite** for local development when PostgreSQL is not configured

### Deployment & Infrastructure

- **Render**
- **Supabase PostgreSQL**
- **WhiteNoise**
- **Git & GitHub**

---

## 🏗️ Project Structure

```text
submitly/
│
├── assignments/
│   ├── migrations/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── courses/
│   ├── migrations/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── submissions/
│   ├── migrations/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests/
│
├── users/
│   ├── migrations/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── static/
│   └── images/
│       └── submitly-logo.png
│
├── templates/
│   └── base.html
│
├── media/
│
├── manage.py
├── requirements.txt
├── build.sh
├── PRD.md
├── AGENTS.md
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Mdsahil01/submitly.git
cd submitly
```

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root if required by your environment.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url
```

For local development without PostgreSQL, Submitly can use SQLite through the Django database configuration.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an administrator

```bash
python manage.py createsuperuser
```

Follow Django's prompts to create the administrator account.

### 7. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 👤 User Roles

Submitly currently supports two application roles.

### Student

Students can:

```text
Register
   ↓
Login
   ↓
Browse Courses
   ↓
Request Enrollment
   ↓
Wait for Faculty Approval
   ↓
Access Course
   ↓
View Assignment
   ↓
Submit Work
   ↓
Receive Marks & Feedback
```

### Faculty

Faculty can:

```text
Login
   ↓
Create Course
   ↓
Approve Students
   ↓
Create Assignment
   ↓
Publish Assignment
   ↓
Receive Submissions
   ↓
Review Work
   ↓
Assign Marks & Feedback
```

---

## 🧪 Testing

Submitly includes automated tests covering authentication, authorization, courses, enrollments, assignments, submissions, evaluation, and student results.

Run the complete test suite:

```bash
python manage.py test
```

Current status:

```text
Ran 90 tests

OK
```

**90/90 tests passing.**

---

## 🔒 Security & Access Control

Submitly uses Django's authentication and authorization mechanisms to protect application functionality.

Examples include:

- Authentication-required dashboards
- Student-only functionality
- Faculty-only functionality
- Faculty ownership validation
- Course enrollment validation
- Assignment publication checks
- Submission ownership checks
- Protected evaluation pages
- File type validation
- File size validation
- CSRF protection through Django forms

Students cannot access faculty-only evaluation functionality, and faculty cannot access student-only dashboard functionality.

---

## 📁 Supported Uploads

### Assignment Reference Files

Faculty can attach:

```text
.pdf
.doc
.docx
.ppt
.pptx
.txt
```

### Student Submissions

Students can upload:

```text
.pdf
.doc
.docx
.ppt
.pptx
.txt
```

Maximum file size:

```text
10 MB
```

---

## 🗄️ Database

Submitly uses Django's ORM and supports PostgreSQL for deployed environments.

The deployed architecture uses:

```text
Submitly
   │
   ├── Django Application
   │
   ├── Gunicorn
   │
   └── PostgreSQL
          │
          └── Supabase
```

SQLite can be used for local development when a PostgreSQL database is not configured.

---

## ☁️ Deployment

The application is configured for deployment using:

- Render for application hosting
- Supabase PostgreSQL for the production database
- Gunicorn as the application server
- WhiteNoise for static file serving

The deployment build process runs:

```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

The application starts with:

```bash
gunicorn config.wsgi:application
```

---

## 🧭 Current Application Flow

### Student

```text
Login / Register
       ↓
Student Dashboard
       ↓
Courses
       ↓
Enrollment Request
       ↓
Approved Course
       ↓
Assignments
       ↓
Assignment Details
       ↓
Submit Assignment
       ↓
Submission Status
       ↓
Result & Feedback
```

### Faculty

```text
Login
  ↓
Faculty Dashboard
  ↓
Courses
  ↓
Enrollment Requests
  ↓
Approve / Reject
  ↓
Create Assignment
  ↓
Publish
  ↓
View Submissions
  ↓
Review Submission
  ↓
Marks & Feedback
```

---

## 📌 Project Status

Submitly has completed its planned core MVP workflow.

### Completed

- Authentication
- Student registration
- Role-based access control
- Student dashboard
- Faculty dashboard
- Course management
- Student enrollment requests
- Faculty enrollment approval/rejection
- Assignment creation
- Assignment publishing
- Assignment reference attachments
- Student submissions
- File validation
- Faculty submission review
- Marks and feedback
- Student results
- Profile page
- Navigation and UI/UX polish
- Submitly branding
- Automated testing

### Test Status

```text
90 / 90 tests passing
```

---

## 🎯 Project Goals

Submitly was built to demonstrate a complete Django web application rather than a collection of isolated features.

The project focuses on:

- Backend architecture with Django
- Database modeling and relationships
- Authentication and authorization
- Role-based application design
- CRUD operations
- File handling
- Form validation
- Automated testing
- PostgreSQL integration
- Production deployment
- UI/UX design
- Git and GitHub workflow

---

## 🔮 Future Improvements

Potential future improvements include:

- Email notifications
- Password reset through email
- Assignment resubmission and version history
- Rich text assignment descriptions
- Advanced faculty analytics
- Submission filtering and sorting
- Cloud object storage for uploaded files
- More advanced profile management
- Improved mobile navigation
- Additional academic roles and workflows

These features are outside the current MVP scope.

---

## 👨‍💻 Author

**Mohammed Sahil**

B.Tech Computer Science Engineering — AI & ML

GitHub: [@Mdsahil01](https://github.com/Mdsahil01)

---

## 📄 License

This project is currently developed as an academic/project application.
