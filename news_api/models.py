from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
USER_TYPES = [
        ('EMP', 'Employee'),
        ('CLI', 'Client'),
    ]

ARTICLE_STATUS = [
        ('DRAF', 'Draft'),
        ('PUBD', 'Published'),
    ]

ARTICLE_COLUMNS = [
        ('MAIN', 'Main'),
        ('POW', 'Power'),
        ('TAX', 'Taxes'),
        ('HLTH', 'Health'),
        ('EN', 'Energy'),
        ('LAB', 'Labor'),
    ]

class AbstractUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    type = models.CharField(max_length=4, choices=USER_TYPES)
    name = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='local_files/profile_pictures/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set when created
    updated_at = models.DateTimeField(auto_now=True) # Automatically set when updated
    
    def __str__(self):
        return self.email
    

class Employee(AbstractUser):
    employee_id = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email

class ClientUser(AbstractUser):
    plan = models.CharField(max_length=200)
    accessible_columns = ArrayField(models.CharField(max_length=4, choices=ARTICLE_COLUMNS), blank=True)
    
    def __str__(self):
        return self.email

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500)
    image = models.ImageField(upload_to='local_files/news_images/', blank=True)
    draft_content = models.TextField() # Content of the article in draft mode (not visible to the public)
    published_content = models.TextField() # Content of the article in published mode (visible to the public)
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set when created
    updated_at = models.DateTimeField(auto_now=True) # Automatically set when updated
    original_publication_at = models.DateTimeField() # Will set the date of the first publication
    last_publication_update_at = models.DateTimeField() # Will set the date of the last update
    author = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, blank=True) # TODO: Make it required
    status = models.CharField(max_length=4, choices=ARTICLE_STATUS)
    column = models.CharField(max_length=4, choices=ARTICLE_COLUMNS)
    
    
