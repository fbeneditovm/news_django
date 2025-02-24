from rest_framework import serializers
from .models import NewsArticle


class NewsArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for NewsArticle model.
    """

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "subtitle",
            "image",
            "draft_content",
            "published_content",
            "created_at",
            "updated_at",
            "original_publication_at",
            "last_publication_update_at",
            "author",
            "status",
            "column",
        ]
        read_only_fields = ["created_at", "updated_at", "author"]
