from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        if user.user_type != 1:
            user.save()
        else:
            raise ValueError('Admins must be created through the admin panel')
        return user

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'), (2, 'Professor'), 
        (3, 'Student'), (4, 'Staff'),
    )
    email = models.EmailField(unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    # Added phone number validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be in format: '+'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        max_length=20, 
        validators=[phone_regex], 
        null=True, 
        blank=True
    )
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','user_type','phone_number','address','date_of_birth','bio']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"

