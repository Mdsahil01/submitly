from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from assignments.models import Assignment
from courses.models import Course, Enrollment

from .models import Submission

User = get_user_model()


class StudentResultsAndFeedbackTests(TestCase):
    """Tests for student results and feedback viewing functionality."""

    def setUp(self):
        self.client = Client()
        
        self.faculty = User.objects.create_user(
            email="faculty@results.com",
            password="FacultyPass123",
            full_name="Results Faculty",
            role="FACULTY",
        )
        
        self.student1 = User.objects.create_user(
            email="student1@results.com",
            password="StudentPass123",
            full_name="Student One",
            role="STUDENT",
        )
        
        self.student2 = User.objects.create_user(
            email="student2@results.com",
            password="StudentPass123",
            full_name="Student Two",
            role="STUDENT",
        )
        
        self.course = Course.objects.create(
            name="Software Engineering",
            code="SE101",
            description="Software Engineering Course",
            faculty=self.faculty,
        )
        
        Enrollment.objects.create(student=self.student1, course=self.course)
        Enrollment.objects.create(student=self.student2, course=self.course)
        
        self.assignment = Assignment.objects.create(
            title="Database Design Assignment",
            description="Design a database schema.",
            course=self.course,
            created_by=self.faculty,
            due_date=timezone.now() + timezone.timedelta(days=7),
            max_marks=Decimal("100.00"),
            is_published=True,
        )
        
        # Create evaluated submission for student1
        self.evaluated_submission = Submission.objects.create(
            student=self.student1,
            assignment=self.assignment,
            content="Database schema design content",
            status=Submission.STATUS_REVIEWED,
            marks=Decimal("85.50"),
            feedback="Excellent work! Your database design demonstrates a strong understanding of normalization.",
            reviewed_at=timezone.now(),
        )
        
        # Create unevaluated submission for student2
        self.pending_submission = Submission.objects.create(
            student=self.student2,
            assignment=self.assignment,
            content="My database schema submission",
            status=Submission.STATUS_SUBMITTED,
        )

    def test_student_can_view_own_evaluated_submission(self):
        """Student can view their own evaluated submission with marks and feedback."""
        self.client.login(username='student1@results.com', password='StudentPass123')
        url = reverse('submissions:submission_detail', args=[self.evaluated_submission.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "85.5")
        self.assertContains(response, "100")
        self.assertContains(response, "Excellent work!")
        self.assertContains(response, "Evaluation Results")

    def test_student_can_see_marks_awarded(self):
        """Student can see the marks they were awarded."""
        self.client.login(username='student1@results.com', password='StudentPass123')
        url = reverse('submissions:submission_detail', args=[self.evaluated_submission.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "85.5")
        self.assertContains(response, "Marks Awarded")

    def test_student_can_see_faculty_feedback(self):
        """Student can see faculty feedback on their submission."""
        self.client.login(username='student1@results.com', password='StudentPass123')
        url = reverse('submissions:submission_detail', args=[self.evaluated_submission.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Faculty Feedback")
        self.assertContains(response, "Excellent work!")
        self.assertContains(response, "normalization")

    def test_student_can_see_reviewed_status(self):
        """Student can see that their submission has been reviewed."""
        self.client.login(username='student1@results.com', password='StudentPass123')
        url = reverse('submissions:submission_detail', args=[self.evaluated_submission.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reviewed")

    def test_student_can_see_reviewed_date(self):
        """Student can see when their submission was reviewed."""
        self.client.login(username='student1@results.com', password='StudentPass123')
        url = reverse('submissions:submission_detail', args=[self.evaluated_submission.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reviewed On")

    def test_student_sees_pending_state_for_unevaluated_submission(self):
        """Student sees evaluation pending message for unevaluated submissions."""
        self.client.login(username='student2@results.com', password='StudentPass123')
        url = reverse('submissions:submission_detail', args=[self.pending_submission.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Evaluation Pending")
        self.assertContains(response, "awaiting review")
        self.assertNotContains(response, "Marks Awarded")

    def test_student_cannot_access_another_students_result(self):
        """Student cannot access another student's submission by changing URL."""
        self.client.login(username='student2@results.com', password='StudentPass123')
        url = reverse('submissions:submission_detail', args=[self.evaluated_submission.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)

