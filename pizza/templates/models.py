from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from datetime import *
#... any other imports

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



class Size(models.Model):
  name = models.CharField(max_length=20)
  price = models.DecimalField(max_digits=4, decimal_places=2, default=1)

  def __str__(self):
    return self.name


class Sauce(models.Model):
  name = models.CharField(max_length=20)
  price = models.DecimalField(max_digits=3, decimal_places=2, default=1)

  def __str__(self):
    return self.name

class Crust(models.Model):
  name = models.CharField(max_length=20)
  price = models.DecimalField(max_digits=3, decimal_places=2, default=1)

  def __str__(self):
    return self.name


class Topping(models.Model):
  name = models.CharField(max_length=20)
  price = models.DecimalField(max_digits=3, decimal_places=2, default=1)

  def __str__(self):
    return self.name

class Cheese(models.Model):
  name = models.CharField(max_length=20)
  price = models.DecimalField(max_digits=3, decimal_places=2, default=1)

  def __str__(self):
    return self.name


class Pizza(models.Model):
  id=models.SmallAutoField(primary_key=True)
  name = models.CharField(max_length=30)
  image = models.ImageField(upload_to='images/', default='images/999-piz-create-your-own.webp')
  price = models.DecimalField(max_digits=4, decimal_places=2, default=12)
  cheese = models.ForeignKey(Cheese, on_delete=models.SET_NULL, null=True, default=1)
  sauce = models.ForeignKey(Sauce, on_delete=models.SET_NULL, null=True, default=1)
  size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, default="2")
  crust = models.ForeignKey(Crust, on_delete=models.SET_NULL, null=True, default=1)
  toppings = models.ManyToManyField(Topping, blank=True)

  def __str__(self):
    return self.name

  def calculate_price(self):
    price = 0;
    for topping in self.toppings.all():
      price += topping.price
    price += (self.crust.price + self.sauce.price + self.size.price)
    return price

class Basket(models.Model):
  basket_id=models.SmallAutoField(primary_key=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  items = models.ManyToManyField(Pizza)
  complete = models.BooleanField(default=False)
  delivery = models.BooleanField(default=True)

  def get_total(self):
    total = 4 * self.delivery
    for pizza in self.items.all():
      total += 10
    return total



class PizzaUser(models.Model):
  id = models.AutoField(primary_key=True)
  basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date_ordered = models.DateTimeField(auto_now_add=True)

  full_name = models.CharField(max_length=200)
  card_number = models.CharField(max_length=16)
  cvv = models.CharField(max_length=4)
  expiry_date = models.CharField(max_length=5)
  address = models.TextField(max_length=200)

  def clean(self):
    super().clean()

      # Validate expiry date is not in the past
    expiry_parts = self.expiry_date.split('/')
    expiry_month = expiry_parts[0]
    expiry_year = expiry_parts[1]
    now = datetime.now()

    if int(expiry_year) < (now.year % 100) or (int(expiry_year) == (now.year % 100) and int(expiry_month) < now.month):
      raise ValidationError('Expiry date cannot be in the past.')

  def save(self, *args, **kwargs):
    self.full_clean()  # Call the full_clean method to run all validations
    super().save(*args, **kwargs)

  def __str__(self):
    return self.full_name
