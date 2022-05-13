from operator import mod
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



class TestingImage(models.Model):
  image_file = models.ImageField(upload_to='images/')  # TODO: give custom name to the image-uploaded as can have duplicates
  person_name = models.CharField(max_length=1000)

class UserProfile(models.Model):
  user_obj = models.ForeignKey(User, on_delete=models.CASCADE)
  
   # both important for activity feed and display on user-profile for everyone
  timestamp_profile_created = models.DateTimeField(auto_now_add=True)
  timestamp_profile_updated = models.DateTimeField(auto_now=True) 

  instagram_id = models.CharField(max_length=2000)
  snapchat_id = models.CharField(max_length=2000)
  spotify_url = models.CharField(max_length=2000)

  gender = models.CharField(max_length=200)
  current_school_status = models.CharField(max_length=1000)
  current_school_campus = models.CharField(max_length=1000)
  current_school_year = models.IntegerField()
  current_college = models.CharField(max_length=2000)
  living_on_res = models.BooleanField(default=False)
  user_location = models.CharField(max_length=2000)
  user_relationship_status = models.CharField(max_length=2000)
  user_pizza_topping = models.CharField(max_length=2000)

  job_companies = models.TextField()
  user_description = models.TextField()
  user_interests = models.TextField()


class UserProfileImage(models.Model):
  user_profile_obj = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
  profile_image = models.ImageField(upload_to='profile_images/', verbose_name='Image')


class UserMajors(models.Model):
  user_profile_obj = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  major = models.CharField(max_length=2000)


class UserCourses(models.Model):
  user_profile_obj = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  course = models.CharField(max_length=2000)






