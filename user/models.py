from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    map_link = models.URLField(max_length=200, null=True, blank=True, help_text="Link to the map of the region")

    def __str__(self):
        return self.name


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    map_link = models.URLField(max_length=200, null=True, blank=True, help_text="Link to the map of the city")

    def __str__(self):
        return f"{self.name}"


class Address(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    map_link = models.URLField(max_length=200, null=True, blank=True, help_text="Link to the specific address location")

    def __str__(self):
        return f"{self.city.name if self.city else 'No City'}, {self.region.name if self.region else 'No Region'}, {self.map_link}"


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('venue', 'Venue Company'),
        ('show', 'Show Company'),
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='user')
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class UserOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField(null=True)
    status = models.CharField(max_length=20, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='profile_images/profile.jpeg')
    phone = models.CharField(max_length=15, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(UserOrder, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
