from django.db import models

from utils.functions import validate_image_file
from utils.global_values import ARTICLE_STATUS, ARTICLE_COLUMNS


# Create your models here.
class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500)
    image = models.ImageField(upload_to="news_images/", validators=[validate_image_file], blank=True)
    draft_content = models.TextField()  # Content of the article in draft mode (not visible to the public)
    published_content = models.TextField()  # Content of the article in published mode (visible to the public)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set when updated
    original_publication_at = models.DateTimeField()  # Will set the date of the first publication
    last_publication_update_at = models.DateTimeField()  # Will set the date of the last update
    author = models.ForeignKey(to="users_api.User", on_delete=models.SET_NULL, null=True)  # Try this format instead
    status = models.CharField(max_length=4, choices=ARTICLE_STATUS)
    column = models.CharField(max_length=4, choices=ARTICLE_COLUMNS, blank=True)
