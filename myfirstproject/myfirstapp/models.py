from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
#... any other imports

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
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


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    bio = models.TextField(null=True) # mark bio as optional

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.get_full_name()

class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    author = models.ForeignKey(Author, null=True ,on_delete = models.CASCADE)
    genre = models.TextField()
    price = models.DecimalField(max_digits=3, decimal_places=2, default=0.0) # 9.99 - 0.00
    
    
class BookUser(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    review = models.TextField(null=True)




class Basket(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)



class BookBasket(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.unit_price