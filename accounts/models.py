from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from enum import IntEnum
from django.conf import settings
from plans.models import Provider
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
class UserType(IntEnum):
    ADMIN = 1
    DISTRIBUTOR = 2
    RETAILER = 3
    CLIENT = 4


class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have a phone number')

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', UserType.ADMIN)

        return self.create_user(email, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        (UserType.ADMIN, 'Admin'),
        (UserType.DISTRIBUTOR, 'Distributor'),
        (UserType.RETAILER, 'Retailer'),
        (UserType.CLIENT, 'Client'),
    ]
    SIM_PROVIDER_CHOICES = [
        ('Airtel', 'Airtel'),
        ('Jio', 'Jio'),
        ('Vi', 'Vi'),
        ('BSNL', 'BSNL'),
    
        ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=UserType.CLIENT)
    sim_provider = models.ForeignKey(
        Provider, on_delete=models.SET_NULL, null=True, blank=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.user_type == UserType.ADMIN

    @property
    def is_distributor(self):
        return self.user_type == UserType.DISTRIBUTOR

    @property
    def is_retailer(self):
        return self.user_type == UserType.RETAILER

    @property
    def is_client(self):
        return self.user_type == UserType.CLIENT

# class User(AbstractUser):
#     USER_TYPE_CHOICES = [
#         (UserType.ADMIN, 'Admin'),
#         (UserType.DISTRIBUTOR, 'Distributor'),
#         (UserType.RETAILER, 'Retailer'),
#         (UserType.CLIENT, 'Client'),
#     ]
#     SIM_PROVIDER_CHOICES = [
#     ('Airtel', 'Airtel'),
#     ('Jio', 'Jio'),
#     ('Vi', 'Vi'),
#     ('BSNL', 'BSNL'),
   
#     ]

#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15, unique=True)
#     user_type = models.IntegerField(
#         choices=USER_TYPE_CHOICES, default=UserType.CLIENT)
#     sim_provider = models.ForeignKey(
#     Provider,
#     on_delete=models.SET_NULL,
#     null=True,
#     blank=True
# )

#     @property
#     def is_admin(self):
#         return self.user_type == UserType.ADMIN

#     @property
#     def is_distributor(self):
#         return self.user_type == UserType.DISTRIBUTOR

#     @property
#     def is_retailer(self):
#         return self.user_type == UserType.RETAILER

#     @property
#     def is_client(self):
#         return self.user_type == UserType.CLIENT

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'phone']

#     def __str__(self):
#         return self.email


class OTP(models.Model):
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=1)
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() < self.expires_at and not self.is_verified

    def __str__(self):
        return f"{self.phone} - {self.code}"


def user_directory_path(instance, filename):
    return f'profile_pictures/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.email
