from django.db import models
from django.utils import timezone
import random
import string
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.
def generate_unique_code():
    length = 8
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if LinkToRegisterPermission.objects.filter(code=code).count() == 0:
            break
    return code


# class LinkToRegisterPermissionManager(models.Manager):
#     def create(self):
#         token = generate_unique_code
#         # expiry = timezone.now() + timedelta(days=1)

#         instance = super(LinkToRegisterPermission, self).create(
#             code=token)
#         return instance, token

class LinkToRegisterPermission(models.Model):
    # objects = LinkToRegisterPermissionManager()
    code = models.CharField(
        max_length=8, default=generate_unique_code, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    # expiry = models.DateTimeField(null=True, blank=Tru

class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password, **extra_fields):
        
        if not username:
            raise ValueError("Username field is required")

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
        # raise ValueError("code no exist")

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


class Person(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_online = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ("created_at",)