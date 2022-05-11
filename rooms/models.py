from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
  use_in_migrations = True

  def _create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError('Users require an email field')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')

    return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
  username = None
  email = models.EmailField(_('email address'), unique=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []



class UserProfile(models.Model):
  gender = models.CharField(max_length=200)
  instagram = models.CharField(max_length=2000)
  snapchat = models.CharField(max_length=2000)
  spotify = models.CharField(max_length=2000)
  current_school_status = models.CharField(max_length=1000)
  current_school_campus = models.CharField(max_length=1000)
  current_school_year = models.IntegerField()
  current_college = models.CharField(max_length=1000)
  living_on_res = models.BooleanField(default=False)



# TODO: 
  # start by adding the list of majors and form submission/saving (**images)
    # need to add 'visibility/privacy' for select-fields




