from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, university_id, password=None, **extra_fields):
        if not university_id:
            raise ValueError('The University ID must be set')
        user = self.model(university_id=university_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, university_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError('Superusers must have a password.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(university_id, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    university_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    has_voted = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'university_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'department']

    def __str__(self):
        return self.university_id
# models.py
class Candidate(models.Model):
    full_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='candidates/')
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.full_name
