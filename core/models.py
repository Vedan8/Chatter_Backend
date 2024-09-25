# core/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from cloudinary.models import CloudinaryField
import cloudinary
from django.core.files.uploadedfile import InMemoryUploadedFile

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None,profileImage=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,profileImage=profileImage, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None,profileImage=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, username,profileImage, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)
    profileImage=CloudinaryField('image', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Upload the image to Cloudinary
        if isinstance(self.profileImage, InMemoryUploadedFile):  # Ensure it's an in-memory file
            upload_result = cloudinary.uploader.upload(self.profileImage)

            # Get the public_id and secure_url from the Cloudinary response
            self.profileImage = upload_result.get('secure_url') 

            # Optionally, you can store the URL in a separate field if needed
            # self.image_url = full_url

        super(User, self).save(*args, **kwargs)  
