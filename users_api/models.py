from typing import Tuple

from django.db import models
from django.contrib.postgres.fields import ArrayField

from utils.functions import validate_image_file
from utils.global_values import USER_TYPES, ARTICLE_COLUMNS

# Create your models here.
class AbcUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    type = models.CharField(max_length=4, choices=USER_TYPES)
    name = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='profile_pictures/', validators=[validate_image_file], blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set when created
    updated_at = models.DateTimeField(auto_now=True) # Automatically set when updated

    class Meta:
        abstract = True  # This makes it an abstract base class in Django's way
    
    def __str__(self):
        return f'Name: {self.name}, Email: {self.email}'

    @staticmethod
    def user_type(self) -> Tuple:
        raise NotImplementedError("Subclasses must implement user_type()")

class Employee(AbcUser):
    employee_id = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    
    def user_type(self) -> Tuple:
        return USER_TYPES[0]

class ClientUser(AbcUser):
    plan = models.CharField(max_length=200)
    accessible_columns = ArrayField(models.CharField(max_length=4, choices=ARTICLE_COLUMNS), blank=True)

    def user_type(self) -> Tuple:
        return USER_TYPES[1]