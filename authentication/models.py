from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
# when creating a new user 
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("Email should be provided")

        email = self.normalize_email(email)

        new_user = self.model(email=email,**extra_fields)

        new_user.set_password(password)
        new_user.save()

        return new_user
# when creating new superuser
    def create_superuser(self,email,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        
        return self.create_user(email,**extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=25,unique=True)
    email = models.EmailField(max_length=80,unique=True)
    phone_number = PhoneNumberField(null=False,unique=True)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username','phone_number']

    def __str__(self):
        return f"<user {self.email}"