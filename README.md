# Submitly

Submitly is an Assignment Submission & Evaluation Platform designed for colleges and academic institutions. It provides a structured, role-based workflow for assignment creation, submission, evaluation, grading, and feedback between faculty and students.

## Project Status

Submitly is actively developed following an issue-driven engineering workflow.

- **Current Milestone:** Authentication & Core Foundation (Completed)
- **Completed Issues:**
  - `#1` — Initialize Submitly Project & Django Architecture
  - `#2` — Establish Custom User Authentication (`users.User`)
  - `#3` — Implement Web Authentication & Role-Based Dashboard Access
- **Next Milestone:** Course & Enrollment Management (`#4`)

## Key Implemented Features

- **Custom User Model:** Email-based authentication with `Student` and `Faculty` role choices.
- **Web Authentication:** Form-based login using Django's built-in `AuthenticationForm` with email/password validation.
- **Secure Session Management:** POST-only logout protecting against CSRF exploits.
- **Role-Based Routing:** Central dashboard dispatcher directing students to `/student/dashboard/` and faculty to `/faculty/dashboard/`.
- **Role-Based Authorization:** Custom `@student_required` and `@faculty_required` decorators enforcing strict HTTP 403 Forbidden responses on unauthorized cross-role requests.
- **Placeholder Dashboards:** Dedicated dashboard views and templates for Students and Faculty.

## Technology Stack

- **Backend:** Python + Django
- **Frontend:** Django Templates + HTML + CSS + JavaScript
- **Database:** SQLite (local development), PostgreSQL-compatible architecture
- **Testing:** Django Test Framework (`unittest`)

## Local Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Mdsahil01/submitly.git
   cd submitly
   ```

2. **Create and Activate a Virtual Environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux:**
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

## Running the Application

Start the local development server:
```bash
python manage.py runserver
```
The application will be accessible at: `http://127.0.0.1:8000/`

## Running Automated Tests

Run the full test suite across all applications:
```bash
python manage.py test
```

## Documentation

- [Product Requirements Document](PRD.md)
- [AI & Engineering Guidelines](AGENTS.md)
- [Engineering Journal](Docs/Engineering%20Journal/)
