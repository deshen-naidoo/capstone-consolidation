"""
Serializers for the News application REST API.
Translates Article models into JSON format.
"""
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.
    Exposes necessary fields for API clients.
    """
    # Flattens the author relationship to just show the username
    author_name = serializers.CharField(
        source='author.username', 
        read_only=True
    )

    class Meta:
        model = Article
        fields =[
            'id', 
            'article_title', 
            'article_content', 
            'author_name', 
            'is_approved'
        ]