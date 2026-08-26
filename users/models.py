from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, role, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not full_name:
            raise ValueError("Users must have a full name")
        if role not in ['STUDENT', 'FACULTY']:
            raise ValueError("Role must be either STUDENT or FACULTY")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, full_name, role, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('FACULTY', 'Faculty'),
    ]

    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name="Email Address"
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name="Full Name"
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        verbose_name="Role"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active Status"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Staff Status"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Joined"
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_student(self):
        return self.role == 'STUDENT'

    @property
    def is_faculty(self):
        return self.role == 'FACULTY'
