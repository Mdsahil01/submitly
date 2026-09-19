from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from courses.models import Course
from users.models import User

from .models import Assignment


class AssignmentModelTests(TestCase):

    def setUp(self):
        self.faculty = User.objects.create_user(
            email="faculty@test.com",
            full_name="Test Faculty",
            role="FACULTY",
            password="Test@123",
        )

        self.other_faculty = User.objects.create_user(
            email="faculty2@test.com",
            full_name="Other Faculty",
            role="FACULTY",
            password="Test@123",
        )

        self.student = User.objects.create_user(
            email="student@test.com",
            full_name="Test Student",
            role="STUDENT",
            password="Test@123",
        )

        self.course = Course.objects.create(
            name="Introduction to Computer Science",
            code="CS101",
            description="Computer Science fundamentals.",
            faculty=self.faculty,
        )

    def create_assignment(self, **kwargs):
        defaults = {
            "title": "Python Basics",
            "description": "Complete the Python basics assignment.",
            "course": self.course,
            "created_by": self.faculty,
            "due_date": timezone.now() + timedelta(days=7),
        }
        defaults.update(kwargs)
        return Assignment.objects.create(**defaults)

    def test_assignment_creation(self):
        assignment = self.create_assignment()

        self.assertEqual(assignment.title, "Python Basics")
        self.assertEqual(assignment.course, self.course)
        self.assertEqual(assignment.created_by, self.faculty)
        self.assertFalse(assignment.is_published)

    def test_assignment_string_representation(self):
        assignment = self.create_assignment()

        self.assertEqual(
            str(assignment),
            "CS101 - Python Basics",
        )

    def test_assignment_has_created_timestamp(self):
        assignment = self.create_assignment()

        self.assertIsNotNone(assignment.created_at)

    def test_non_faculty_cannot_create_assignment(self):
        assignment = self.create_assignment(
            created_by=self.student,
        )

        with self.assertRaises(ValidationError):
            assignment.full_clean()

    def test_faculty_cannot_create_assignment_for_another_faculty_course(self):
        assignment = self.create_assignment(
            created_by=self.other_faculty,
        )

        with self.assertRaises(ValidationError):
            assignment.full_clean()

    def test_faculty_can_create_assignment_for_own_course(self):
        assignment = self.create_assignment()

        try:
            assignment.full_clean()
        except ValidationError:
            self.fail("Faculty should be able to create assignments for their own course.")

    def test_published_status_defaults_to_false(self):
        assignment = self.create_assignment()

        self.assertFalse(assignment.is_published)

    def test_assignment_course_relationship(self):
        assignment = self.create_assignment()

        self.assertIn(assignment, self.course.assignments.all())