from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self , email ,password , **extra_fields):
        
        if not email:
            raise ValueError(_("The Email Must Be Set"))
        email = self.normalize_email(email)
        user = self.model(email=email , **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault('is_staff' , True)
        extra_fields.setdefault('is_superuser' , True)
        extra_fields.setdefault('is_active' , True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Super User Must Have is_staff==True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email , password , **extra_fields)
    



class User(AbstractBaseUser , PermissionsMixin):
    email = models.EmailField(unique=True , max_length=255)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    first_name = models.CharField(max_length=20)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"