from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_student_user(self):
        user = User.objects.create_user(
            email='student@college.edu',
            full_name='Jane Student',
            role='STUDENT',
            password='testpassword123'
        )
        self.assertEqual(user.email, 'student@college.edu')
        self.assertEqual(user.full_name, 'Jane Student')
        self.assertEqual(user.role, 'STUDENT')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_student)
        self.assertFalse(user.is_faculty)
        self.assertTrue(user.check_password('testpassword123'))

    def test_create_faculty_user(self):
        user = User.objects.create_user(
            email='faculty@college.edu',
            full_name='Dr. Sarah Faculty',
            role='FACULTY',
            password='testpassword123'
        )
        self.assertEqual(user.email, 'faculty@college.edu')
        self.assertEqual(user.full_name, 'Dr. Sarah Faculty')
        self.assertEqual(user.role, 'FACULTY')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_student)
        self.assertTrue(user.is_faculty)

    def test_create_user_invalid_role(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='invalid@college.edu',
                full_name='Invalid User',
                role='ADMIN',
                password='testpassword123'
            )

    def test_create_user_missing_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                full_name='No Email User',
                role='STUDENT',
                password='testpassword123'
            )

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='admin@college.edu',
            full_name='Admin User',
            role='FACULTY',
            password='testpassword123'
        )
        self.assertEqual(user.email, 'admin@college.edu')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_authenticate_user(self):
        User.objects.create_user(
            email='auth@college.edu',
            full_name='Auth Test',
            role='STUDENT',
            password='securepassword'
        )
        # Verify authentication via email
        user = authenticate(username='auth@college.edu', password='securepassword')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'auth@college.edu')

        # Verify authentication failure with wrong password
        failed_user = authenticate(username='auth@college.edu', password='wrongpassword')
        self.assertIsNone(failed_user)

