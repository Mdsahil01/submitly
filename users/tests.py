from django.test import TestCase, Client
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse

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


class WebAuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(
            email='student@college.edu',
            full_name='Jane Student',
            role='STUDENT',
            password='studentpassword123'
        )
        self.faculty = User.objects.create_user(
            email='faculty@college.edu',
            full_name='Dr. Sarah Faculty',
            role='FACULTY',
            password='facultypassword123'
        )

    def test_login_page_renders_form(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'Log In')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')

    def test_student_login_success_and_redirect(self):
        response = self.client.post(reverse('login'), {
            'username': 'student@college.edu',
            'password': 'studentpassword123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/student_dashboard.html')
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].email, 'student@college.edu')

    def test_faculty_login_success_and_redirect(self):
        response = self.client.post(reverse('login'), {
            'username': 'faculty@college.edu',
            'password': 'facultypassword123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/faculty_dashboard.html')
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].email, 'faculty@college.edu')

    def test_login_with_next_parameter(self):
        target_url = reverse('student_dashboard')
        response = self.client.post(
            f"{reverse('login')}?next={target_url}",
            {
                'username': 'student@college.edu',
                'password': 'studentpassword123'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/student_dashboard.html')

    def test_login_invalid_password_fails(self):
        response = self.client.post(reverse('login'), {
            'username': 'student@college.edu',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTrue(response.context['form'].errors)

    def test_login_nonexistent_user_fails(self):
        response = self.client.post(reverse('login'), {
            'username': 'nonexistent@college.edu',
            'password': 'somepassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTrue(response.context['form'].errors)

    def test_authenticated_user_accessing_login_redirects(self):
        self.client.login(username='student@college.edu', password='studentpassword123')
        response = self.client.get(reverse('login'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/student_dashboard.html')

    def test_logout_post_succeeds_and_ends_session(self):
        self.client.login(username='student@college.edu', password='studentpassword123')
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_get_method_not_allowed(self):
        self.client.login(username='student@college.edu', password='studentpassword123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)


class RootAndDashboardRoutingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(
            email='student@college.edu',
            full_name='Jane Student',
            role='STUDENT',
            password='studentpassword123'
        )
        self.faculty = User.objects.create_user(
            email='faculty@college.edu',
            full_name='Dr. Sarah Faculty',
            role='FACULTY',
            password='facultypassword123'
        )

    def test_root_unauthenticated_redirects_to_login(self):
        response = self.client.get(reverse('root'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_root_authenticated_student_redirects_to_dashboard(self):
        self.client.login(username='student@college.edu', password='studentpassword123')
        response = self.client.get(reverse('root'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/student_dashboard.html')

    def test_root_authenticated_faculty_redirects_to_dashboard(self):
        self.client.login(username='faculty@college.edu', password='facultypassword123')
        response = self.client.get(reverse('root'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/faculty_dashboard.html')

    def test_dashboard_redirect_unauthenticated(self):
        response = self.client.get(reverse('dashboard_redirect'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_dashboard_redirect_student(self):
        self.client.login(username='student@college.edu', password='studentpassword123')
        response = self.client.get(reverse('dashboard_redirect'))
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_dashboard_redirect_faculty(self):
        self.client.login(username='faculty@college.edu', password='facultypassword123')
        response = self.client.get(reverse('dashboard_redirect'))
        self.assertRedirects(response, reverse('faculty_dashboard'))


class RoleBasedAccessControlTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(
            email='student@college.edu',
            full_name='Jane Student',
            role='STUDENT',
            password='studentpassword123'
        )
        self.faculty = User.objects.create_user(
            email='faculty@college.edu',
            full_name='Dr. Sarah Faculty',
            role='FACULTY',
            password='facultypassword123'
        )

    def test_student_dashboard_requires_login(self):
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_faculty_dashboard_requires_login(self):
        response = self.client.get(reverse('faculty_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_student_can_access_student_dashboard(self):
        self.client.login(username='student@college.edu', password='studentpassword123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/student_dashboard.html')
        self.assertContains(response, 'Jane Student')
        self.assertContains(response, 'Student Dashboard')

    def test_student_forbidden_from_faculty_dashboard(self):
        self.client.login(username='student@college.edu', password='studentpassword123')
        response = self.client.get(reverse('faculty_dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_faculty_can_access_faculty_dashboard(self):
        self.client.login(username='faculty@college.edu', password='facultypassword123')
        response = self.client.get(reverse('faculty_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/faculty_dashboard.html')
        self.assertContains(response, 'Dr. Sarah Faculty')
        self.assertContains(response, 'Faculty Dashboard')

    def test_faculty_forbidden_from_student_dashboard(self):
        self.client.login(username='faculty@college.edu', password='facultypassword123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 403)
