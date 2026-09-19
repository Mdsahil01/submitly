from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from .models import Course, Enrollment

User = get_user_model()


class CourseModelTests(TestCase):
    def setUp(self):
        self.faculty = User.objects.create_user(
            email='faculty@college.edu',
            full_name='Dr. Sarah Faculty',
            role='FACULTY',
            password='testpassword123'
        )
        self.student = User.objects.create_user(
            email='student@college.edu',
            full_name='Jane Student',
            role='STUDENT',
            password='testpassword123'
        )

    def test_create_course_success(self):
        course = Course.objects.create(
            name='Introduction to Computer Science',
            code='CS101',
            description='Foundational CS concepts and programming.',
            faculty=self.faculty
        )
        self.assertEqual(course.name, 'Introduction to Computer Science')
        self.assertEqual(course.code, 'CS101')
        self.assertEqual(course.description, 'Foundational CS concepts and programming.')
        self.assertEqual(course.faculty, self.faculty)
        self.assertIsNotNone(course.created_at)

    def test_course_str_representation(self):
        course = Course.objects.create(
            name='Data Structures',
            code='CS102',
            faculty=self.faculty
        )
        self.assertEqual(str(course), 'CS102 - Data Structures')

    def test_duplicate_course_code_raises_integrity_error(self):
        Course.objects.create(
            name='First Course',
            code='CS101',
            faculty=self.faculty
        )
        with self.assertRaises(IntegrityError):
            Course.objects.create(
                name='Second Course',
                code='CS101',
                faculty=self.faculty
            )

    def test_course_clean_valid_faculty(self):
        course = Course(
            name='Algorithms',
            code='CS201',
            faculty=self.faculty
        )
        # Should not raise any ValidationError
        course.full_clean()

    def test_course_clean_invalid_faculty_role_raises_validation_error(self):
        course = Course(
            name='Invalid Course Owner',
            code='CS999',
            faculty=self.student
        )
        with self.assertRaises(ValidationError) as context:
            course.full_clean()
        self.assertIn('faculty', context.exception.message_dict)

    def test_faculty_courses_reverse_relationship(self):
        course1 = Course.objects.create(
            name='Course One',
            code='CS101',
            faculty=self.faculty
        )
        course2 = Course.objects.create(
            name='Course Two',
            code='CS102',
            faculty=self.faculty
        )
        self.assertEqual(self.faculty.courses.count(), 2)
        self.assertIn(course1, self.faculty.courses.all())
        self.assertIn(course2, self.faculty.courses.all())


class EnrollmentModelTests(TestCase):
    def setUp(self):
        self.faculty = User.objects.create_user(
            email='faculty@college.edu',
            full_name='Dr. Sarah Faculty',
            role='FACULTY',
            password='testpassword123'
        )
        self.student = User.objects.create_user(
            email='student@college.edu',
            full_name='Jane Student',
            role='STUDENT',
            password='testpassword123'
        )
        self.course = Course.objects.create(
            name='Introduction to Computer Science',
            code='CS101',
            faculty=self.faculty
        )

    def test_create_enrollment_success(self):
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.course, self.course)
        self.assertIsNotNone(enrollment.enrolled_at)

    def test_enrollment_str_representation(self):
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        self.assertEqual(str(enrollment), 'Jane Student enrolled in CS101')

    def test_duplicate_enrollment_raises_integrity_error(self):
        Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(
                student=self.student,
                course=self.course
            )

    def test_enrollment_clean_valid_student(self):
        enrollment = Enrollment(
            student=self.student,
            course=self.course
        )
        # Should not raise any ValidationError
        enrollment.full_clean()

    def test_enrollment_clean_invalid_student_role_raises_validation_error(self):
        other_faculty = User.objects.create_user(
            email='other_faculty@college.edu',
            full_name='Dr. Mark Other',
            role='FACULTY',
            password='testpassword123'
        )
        enrollment = Enrollment(
            student=other_faculty,
            course=self.course
        )
        with self.assertRaises(ValidationError) as context:
            enrollment.full_clean()
        self.assertIn('student', context.exception.message_dict)

    def test_student_and_course_reverse_relationships(self):
        course2 = Course.objects.create(
            name='Web Development',
            code='CS103',
            faculty=self.faculty
        )
        enrollment1 = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        enrollment2 = Enrollment.objects.create(
            student=self.student,
            course=course2
        )
        self.assertEqual(self.student.enrollments.count(), 2)
        self.assertIn(enrollment1, self.student.enrollments.all())
        self.assertIn(enrollment2, self.student.enrollments.all())
        self.assertEqual(self.course.enrollments.count(), 1)
        self.assertIn(enrollment1, self.course.enrollments.all())


class CascadeDeletionTests(TestCase):
    def setUp(self):
        self.faculty = User.objects.create_user(
            email='faculty@college.edu',
            full_name='Dr. Sarah Faculty',
            role='FACULTY',
            password='testpassword123'
        )
        self.student = User.objects.create_user(
            email='student@college.edu',
            full_name='Jane Student',
            role='STUDENT',
            password='testpassword123'
        )
        self.course = Course.objects.create(
            name='Introduction to Computer Science',
            code='CS101',
            faculty=self.faculty
        )
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )

    def test_course_deletion_cascades_to_enrollments(self):
        course_id = self.course.id
        enrollment_id = self.enrollment.id
        self.course.delete()

        self.assertFalse(Course.objects.filter(id=course_id).exists())
        self.assertFalse(Enrollment.objects.filter(id=enrollment_id).exists())
        # Student and faculty must remain intact
        self.assertTrue(User.objects.filter(id=self.student.id).exists())
        self.assertTrue(User.objects.filter(id=self.faculty.id).exists())

    def test_student_deletion_cascades_to_enrollments(self):
        student_id = self.student.id
        enrollment_id = self.enrollment.id
        self.student.delete()

        self.assertFalse(User.objects.filter(id=student_id).exists())
        self.assertFalse(Enrollment.objects.filter(id=enrollment_id).exists())
        # Course and faculty must remain intact
        self.assertTrue(Course.objects.filter(id=self.course.id).exists())
        self.assertTrue(User.objects.filter(id=self.faculty.id).exists())

    def test_faculty_deletion_cascades_to_courses_and_enrollments(self):
        faculty_id = self.faculty.id
        course_id = self.course.id
        enrollment_id = self.enrollment.id
        self.faculty.delete()

        self.assertFalse(User.objects.filter(id=faculty_id).exists())
        self.assertFalse(Course.objects.filter(id=course_id).exists())
        self.assertFalse(Enrollment.objects.filter(id=enrollment_id).exists())
        # Student must remain intact
        self.assertTrue(User.objects.filter(id=self.student.id).exists())
