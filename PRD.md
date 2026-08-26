````markdown
# Submitly — Product Requirements Document (PRD)

**Product Name:** Submitly  
**Product Type:** Web Application  
**Product Category:** Assignment Submission & Evaluation Platform  
**Status:** Initial Product Definition  
**Version:** 1.0

---

## 1. Product Overview

Submitly is a web-based assignment submission and evaluation platform designed for colleges and academic institutions.

The platform manages the complete assignment lifecycle between faculty and students:

> **Create → Write → Submit → Review → Grade → Feedback → Improve / Resubmit**

Submitly focuses specifically on the assignment workflow rather than attempting to become a complete Learning Management System (LMS).

---

## 2. Problem Statement

Assignment management in colleges can involve multiple disconnected processes:

- Faculty distributes assignment instructions through different channels.
- Students submit files through email, messaging applications, or physical copies.
- Faculty must manually organize submitted files.
- Students may not know whether their submission was successfully received.
- Grades and feedback may be communicated separately from the submitted work.
- Managing late submissions and multiple submissions can become difficult.

Submitly aims to provide a centralized workflow for assignment creation, submission, evaluation, grading, and feedback.

---

## 3. Goals

### Primary Goals

1. Provide faculty with a centralized system for creating and managing assignments.
2. Allow students to view available assignments and their deadlines.
3. Allow students to securely upload assignment submissions.
4. Support common academic submission formats.
5. Allow faculty to review student submissions.
6. Allow faculty to assign marks and provide feedback.
7. Allow students to view their evaluation results.
8. Track submission status and submission time.
9. Provide a clean and understandable user experience.
10. Build the application using a maintainable full-stack architecture.

### Secondary Goals

- Support submission history and resubmission.
- Detect late submissions.
- Provide structured evaluation in future iterations.
- Make the architecture extensible for future LMS-related features.

---

## 4. Target Users

Submitly has two primary user roles.

### 4.1 Student

Students use Submitly to:

- Log in to their account.
- View assignments.
- Read assignment instructions.
- View deadlines.
- Download assignment resources.
- Upload submissions.
- View submission status.
- View marks.
- View faculty feedback.
- Resubmit work when permitted.

### 4.2 Faculty

Faculty members use Submitly to:

- Log in to their account.
- Create assignments.
- Edit assignments.
- Set assignment deadlines.
- Attach assignment/reference files.
- View student submissions.
- Review submitted files.
- Assign marks.
- Provide feedback.
- Track reviewed and pending submissions.

---

## 5. Core Assignment Lifecycle

The central workflow of Submitly is:

```text
Faculty
   │
   ▼
Create Assignment
   │
   ▼
Publish Assignment
   │
   ▼
Student Views Assignment
   │
   ▼
Student Works on Assignment
   │
   ▼
Student Uploads Submission
   │
   ▼
Submission Recorded
   │
   ▼
Faculty Reviews Submission
   │
   ▼
Faculty Assigns Marks
   │
   ▼
Faculty Provides Feedback
   │
   ▼
Student Views Result
   │
   ▼
Improve / Resubmit (when allowed)
````

This lifecycle is the central product experience.

---

## 6. Functional Requirements

### 6.1 Authentication

The system shall provide authentication for users.

The system shall distinguish between:

- Student
- Faculty

Users shall only access functionality permitted for their role.

---

### 6.2 Assignment Management

Faculty shall be able to:

- Create an assignment.
- Enter an assignment title.
- Enter assignment instructions/description.
- Select or specify a course/subject.
- Set a deadline.
- Specify maximum marks.
- Attach reference/question files.
- Publish an assignment.
- Edit an assignment when permitted.
- View assignment details.

Students shall be able to:

- View assignments available to them.
- View assignment instructions.
- View the deadline.
- View maximum marks.
- Download attached assignment/reference files.

---

### 6.3 Assignment Submission

Students shall be able to submit assignments through the web application.

Supported submission formats:

- `.pdf`
- `.doc`
- `.docx`
- `.ppt`
- `.pptx`

The system shall validate:

- File type.
- File size.
- Submission eligibility.
- Assignment availability.

The system shall record:

- Student.
- Assignment.
- Uploaded file.
- Submission timestamp.
- Submission status.
- Whether the submission was late.

---

### 6.4 Submission Status

Students shall be able to see the current state of their submission.

Possible states include:

```text
Not Submitted
Submitted
Late
Under Review
Reviewed
```

The exact status model may be refined during architecture design.

---

### 6.5 Faculty Evaluation

Faculty shall be able to:

- View submissions for an assignment.
- Identify students who have and have not submitted.
- Open/download submitted files.
- Enter marks.
- Enter feedback.
- Save an evaluation.
- Update an evaluation when permitted.

---

### 6.6 Student Results

After evaluation, students shall be able to view:

- Marks obtained.
- Maximum marks.
- Faculty feedback.
- Evaluation status.
- Evaluation timestamp where applicable.

Students shall not be able to modify marks or faculty feedback.

---

### 6.7 Resubmission

The system should support resubmission when enabled by faculty.

When resubmission is allowed:

- A student may upload a newer version.
- The system should preserve previous submission records.
- The latest valid submission should be clearly identifiable.
- Faculty should be able to distinguish between submission versions.

Detailed version-history behavior will be finalized during architecture design.

---

## 7. File Management Requirements

### Student Submission Formats

Submitly shall support:

```text
PDF
DOC
DOCX
PPT
PPTX
```

### Assignment Resource Formats

Faculty assignment/reference files may use the same supported formats where appropriate.

### File Validation

The application shall validate:

- Extension.
- MIME/content type where practical.
- Maximum file size.
- User permissions.
- Assignment state.

The system should provide clear error messages when an upload is rejected.

---

## 8. Permissions & Security

Submitly must enforce role-based access.

### Student

A student may:

- View assignments available to them.
- Submit their own assignments.
- View their own submissions.
- View their own marks and feedback.

A student must **not** be able to:

- View another student's submission.
- Modify another student's submission.
- Change marks.
- Change faculty feedback.
- Access faculty-only functionality.

### Faculty

Faculty may:

- Create and manage assignments they are authorized to manage.
- View authorized student submissions.
- Evaluate submissions.
- Provide marks and feedback.

Faculty must not be able to access unrelated data without authorization.

---

## 9. Main Screens

### Public

- Landing page
- Login

### Student

- Student Dashboard
- Assignment List
- Assignment Details
- Submission Page
- Submission Status
- Submission History
- Evaluation / Result

### Faculty

- Faculty Dashboard
- Assignment List
- Create Assignment
- Edit Assignment
- Assignment Details
- Submission List
- Submission Review
- Evaluation Form

---

## 10. MVP Scope

The Minimum Viable Product shall include:

### Authentication

- Student login
- Faculty login
- Role-based access

### Assignment Management

- Faculty creates assignment
- Faculty sets deadline
- Faculty provides instructions
- Student views assignment

### Submission

- Student uploads assignment
- PDF/DOC/DOCX/PPT/PPTX validation
- Submission timestamp
- Submission status
- Late submission detection

### Evaluation

- Faculty views submissions
- Faculty gives marks
- Faculty provides feedback
- Student views marks and feedback

### Basic UI

- Student dashboard
- Faculty dashboard
- Assignment pages
- Submission pages
- Evaluation pages

---

## 11. Features Outside Initial MVP

The following features are intentionally excluded from the initial MVP:

- Attendance management
- Full course management
- Timetables
- Online examinations
- Messaging/chat
- Notifications system
- Payment systems
- AI grading
- Automated plagiarism detection
- Advanced analytics
- Mobile applications
- Complete LMS functionality

These may be considered in future versions.

---

## 12. Differentiating Features

Submitly should not attempt to compete with a complete LMS such as Moodle in scope.

Its focus is the assignment lifecycle.

Potential differentiating features include:

### Submission Version History

Students can submit multiple versions when resubmission is permitted.

Faculty can see previous versions rather than having them silently overwritten.

### Structured Evaluation

Future versions may allow faculty to evaluate using a rubric, for example:

```text
Understanding       20
Implementation      30
Documentation       20
Presentation        10
-----------------------
Total               80
```

### Clear Submission Lifecycle

The system should make the state of an assignment obvious:

```text
Not Submitted
     ↓
Submitted
     ↓
Under Review
     ↓
Reviewed
     ↓
Feedback Available
```

These features should be implemented only after the core MVP is stable.

---

## 13. Technology Stack

### Backend

**Python + Django**

Django will handle:

- Application logic
- Authentication
- Routing
- Database interaction
- Form handling
- File upload processing
- Permissions

### Frontend

**Django Templates + HTML + CSS + JavaScript**

The initial application will not use React or another frontend framework.

The frontend should remain modular enough that a separate frontend could be introduced in the future if required.

### Database

**SQLite**

SQLite will be used for local development and initial implementation.

The application architecture should remain compatible with:

**PostgreSQL**

for production deployment.

### Static Files

Django static-file handling will be used for:

- CSS
- JavaScript
- Images
- Other frontend assets

### Uploaded Files

Assignment and submission files must be treated as persistent application data.

Production storage should not rely on an ephemeral deployment filesystem.

### Deployment

Initial deployment target:

**Vercel**

Production database and persistent file storage requirements must be addressed before deployment.

---

## 14. Development Principles

Submitly will be developed as a real software project rather than as a single generated codebase.

Development principles:

1. Keep the architecture simple and understandable.
2. Prefer Django's built-in functionality when appropriate.
3. Avoid unnecessary dependencies.
4. Implement features incrementally.
5. Use GitHub Issues for development tasks.
6. Keep issues small and focused.
7. Test functionality as it is implemented.
8. Maintain clear separation between users, assignments, submissions, and evaluation.
9. Never bypass authorization checks for convenience.
10. Do not introduce features outside the current issue without discussion.

---

## 15. Development Workflow

The project will follow issue-based development.

The general workflow is:

```text
Product Requirement
       ↓
GitHub Issue
       ↓
Implementation Plan
       ↓
Antigravity Implementation
       ↓
Testing
       ↓
Code Review
       ↓
Commit
       ↓
Pull Request / Merge
       ↓
Issue Closed
```

Antigravity will act as an implementation agent.

Product decisions and architectural decisions must be reviewed before implementation.

---

## 16. Initial Development Milestones

### Milestone 1 — Foundation

- Project initialization
- Django configuration
- Development environment
- Git setup

### Milestone 2 — Authentication

- User authentication
- Student role
- Faculty role
- Permissions

### Milestone 3 — Assignment Management

- Assignment model
- Faculty assignment creation
- Assignment editing
- Student assignment viewing

### Milestone 4 — Submission System

- Submission model
- File uploads
- File validation
- Submission status
- Deadline handling

### Milestone 5 — Evaluation

- Faculty submission review
- Marks
- Feedback
- Student results

### Milestone 6 — Product Experience

- Student dashboard
- Faculty dashboard
- Responsive UI
- Error states
- Empty states
- Loading states

### Milestone 7 — Quality & Deployment

- Automated tests
- Security review
- Production database
- Persistent file storage
- Vercel deployment
- Production verification

---

## 17. Success Criteria

Submitly will be considered successful when:

1. A faculty user can create an assignment.
2. A student can view that assignment.
3. The student can submit a valid PDF, DOC, DOCX, PPT, or PPTX file.
4. The system records the submission correctly.
5. The system identifies late submissions.
6. Faculty can access authorized student submissions.
7. Faculty can assign marks.
8. Faculty can provide feedback.
9. Students can view their evaluation.
10. Unauthorized users cannot access protected data.
11. The complete workflow can be demonstrated from assignment creation through evaluation.
12. The application can be deployed successfully.

---

## 18. Non-Goals

Submitly is not intended, in its initial version, to be:

- A complete Moodle replacement.
- A complete Learning Management System.
- A video-learning platform.
- An online examination platform.
- An attendance management system.
- An AI grading system.

The product will remain focused on:

> **Assignment submission and evaluation.**

---

## 19. Product Vision

Submitly begins as a focused assignment submission platform.

Its long-term direction is to become a simple, reliable academic work-management platform centered around the lifecycle of student work:

> **Create → Work → Submit → Review → Evaluate → Improve**

The initial product should solve this workflow exceptionally well before expanding into broader LMS functionality.

```
```