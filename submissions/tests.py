from datetime import timedelta
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from assignments.models import Assignment
from courses.models import Course, Enrollment
from submissions.models import Submission
from users.models import User

class SubmissionModelTests(TestCase):

    def setUp(self):
        self.faculty = User.objects.create_user(
            email="faculty@test.com",
            password="Test@123",
            full_name="Test Faculty",
            role="FACULTY",
        )

        self.student = User.objects.create_user(
            email="student@test.com",
            password="Test@123",
            full_name="Test Student",
            role="STUDENT",
        )

        self.other_student = User.objects.create_user(
            email="other@test.com",
            password="Test@123",
            full_name="Other Student",
            role="STUDENT",
        )

        self.course = Course.objects.create(
            name="Computer Science",
            code="CS999",
            description="Test course",
            faculty=self.faculty,
        )

        Enrollment.objects.create(
            student=self.student,
            course=self.course,
        )

        self.assignment = Assignment.objects.create(
            title="Python Assignment",
            description="Write a Python program.",
            course=self.course,
            created_by=self.faculty,
            due_date=timezone.now() + timedelta(days=2),
            is_published=True,
        )

    def test_submission_creation(self):
        submission = Submission.objects.create(
            student=self.student,
            assignment=self.assignment,
            content="print('Hello World')",
        )

        self.assertEqual(submission.student, self.student)
        self.assertEqual(submission.assignment, self.assignment)
        self.assertEqual(submission.content, "print('Hello World')")
        self.assertEqual(submission.status, Submission.STATUS_SUBMITTED)
        self.assertIsNotNone(submission.submitted_at)

    def test_submission_string_representation(self):
        submission = Submission.objects.create(
            student=self.student,
            assignment=self.assignment,
            content="Test submission",
        )

        self.assertEqual(
            str(submission),
            "Test Student - Python Assignment",
        )

    def test_student_can_submit_for_enrolled_course(self):
        submission = Submission(
            student=self.student,
            assignment=self.assignment,
            content="My answer",
        )

        submission.full_clean()
        submission.save()

        self.assertEqual(Submission.objects.count(), 1)

    def test_unenrolled_student_cannot_submit(self):
        submission = Submission(
            student=self.other_student,
            assignment=self.assignment,
            content="Unauthorized answer",
        )

        with self.assertRaises(ValidationError):
            submission.full_clean()

    def test_unpublished_assignment_cannot_be_submitted(self):
        self.assignment.is_published = False
        self.assignment.save()

        submission = Submission(
            student=self.student,
            assignment=self.assignment,
            content="My answer",
        )

        with self.assertRaises(ValidationError):
            submission.full_clean()

    def test_duplicate_submission_is_prevented(self):
        Submission.objects.create(
            student=self.student,
            assignment=self.assignment,
            content="First answer",
        )

        with self.assertRaises(Exception):
            Submission.objects.create(
                student=self.student,
                assignment=self.assignment,
                content="Second answer",
            )

    def test_submission_belongs_to_assignment(self):
        submission = Submission.objects.create(
            student=self.student,
            assignment=self.assignment,
            content="My answer",
        )

        self.assertEqual(
            submission.assignment.course,
            self.course,
        )

    def test_submission_status_defaults_to_submitted(self):
        submission = Submission.objects.create(
            student=self.student,
            assignment=self.assignment,
            content="My answer",
        )

        self.assertEqual(
            submission.status,
            Submission.STATUS_SUBMITTED,
        )

    def test_submission_with_file_upload(self):
        test_file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )

        submission = Submission.objects.create(
            student=self.student,
            assignment=self.assignment,
            content="My answer with file",
            file=test_file,
        )

        self.assertIsNotNone(submission.file)
        self.assertEqual(submission.file_name, "test.pdf")

    def test_submission_with_invalid_file_type(self):
        test_file = SimpleUploadedFile(
            "test.exe",
            b"file_content",
            content_type="application/x-msdownload"
        )

        submission = Submission(
            student=self.student,
            assignment=self.assignment,
            content="My answer",
            file=test_file,
        )

        with self.assertRaises(ValidationError) as context:
            submission.full_clean()
        
        self.assertIn("file", str(context.exception))

    def test_late_submission_status(self):
        past_assignment = Assignment.objects.create(
            title="Past Assignment",
            description="This is past due.",
            course=self.course,
            created_by=self.faculty,
            due_date=timezone.now() - timedelta(hours=1),
            is_published=True,
        )

        submission = Submission(
            student=self.student,
            assignment=past_assignment,
            content="Late submission",
        )

        # Save should set status to LATE
        submission.save()

        self.assertEqual(submission.status, Submission.STATUS_LATE)

    def test_submission_content_can_be_blank(self):
        test_file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )

        submission = Submission.objects.create(
            student=self.student,
            assignment=self.assignment,
            content="",
            file=test_file,
        )

        submission.full_clean()
        self.assertEqual(submission.content, "")

    def test_allowed_file_extensions(self):
        allowed_extensions = [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".txt"]
        
        for ext in allowed_extensions:
            test_file = SimpleUploadedFile(
                f"test{ext}",
                b"file_content",
                content_type="application/octet-stream"
            )

            submission = Submission(
                student=self.student,
                assignment=self.assignment,
                content="Test",
                file=test_file,
            )

            try:
                submission.full_clean()
            except ValidationError:
                self.fail(f"File with extension {ext} should be allowed")