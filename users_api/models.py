from typing import Tuple

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from utils.functions import validate_image_file
from utils.global_values import USER_PROFILES, ARTICLE_COLUMNS, PLANS


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    user_profile = models.CharField(max_length=4, choices=USER_PROFILES)
    profile_picture = models.ImageField(upload_to="profile_pictures/", validators=[validate_image_file], blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    employee_id = models.CharField(max_length=200, blank=True)
    plan = models.CharField(max_length=4, choices=PLANS, blank=True, default=PLANS[0][0])
    accessible_columns = ArrayField(models.CharField(max_length=4, choices=ARTICLE_COLUMNS), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    @classmethod
    def get_class_user_profile(cls) -> Tuple:
        raise NotImplementedError("Subclasses must implement this method")

    def __str__(self):
        return f"User ID: {self.id}, Name: {self.name}, Email: {self.email}"

    @property
    def is_employee(self):
        return self.user_profile == USER_PROFILES[0][0]  # Assuming first profile is employee

    @property
    def is_client(self):
        return self.user_profile == USER_PROFILES[1][0]  # Assuming second profile is client

    class Meta:
        app_label = "users_api"
