from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    photo = models.ImageField()
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_technician = models.BooleanField(default=False)
    is_scientist = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, obj=None):
        return self.is_admin


