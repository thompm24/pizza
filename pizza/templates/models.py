from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
#... any other imports

class Size(models.Model):
  id=models.SmallAutoField(primary_key=True)
  name = models.CharField(max_length=10)
  price_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1)

class Pizza(models.Model):
  id=models.SmallAutoField(primary_key=True)
  name = models.CharField(max_length=30)
  price = models.DecimalField(max_digits=4, decimal_places=2, default=12)
  image = models.ImageField(upload_to='images/')

class UserManager(BaseUserManager):
  use_in_migrations = True

  def _create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError('The given email must be set')
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
  email = models.EmailField('Email', unique=True)
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  objects = UserManager()
