"""
Database models for the News Application.
Defines Publishers, CustomUsers, Articles, and Newsletters.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class Publisher(models.Model):
    """
    Represents a publishing entity that employs editors 
    and journalists.
    """
    publisher_name = models.CharField(max_length=200)

    def __str__(self):
        """Returns the name of the publisher."""
        return self.publisher_name

class CustomUser(AbstractUser):
    """
    Custom user model handling Readers, Editors, and Journalists.
    Manages specific fields based on the assigned role.
    """
    ROLE_OPTIONS =[
        ('Reader', 'Reader'),
        ('Editor', 'Editor'),
        ('Journalist', 'Journalist'),
    ]
    
    user_role = models.CharField(
        max_length=50, 
        choices=ROLE_OPTIONS, 
        default='Reader'
    )
    
    # Affiliation for Editors and Journalists
    publisher_affiliation = models.ForeignKey(
        Publisher, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    # Reader specific fields
    subscribed_publishers = models.ManyToManyField(
        Publisher, 
        related_name='reader_subscribers', 
        blank=True
    )
    subscribed_journalists = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        blank=True
    )

    def clean(self):
        """
        Robustness: Validates data before saving to database.
        Enforces the "assign fields a value of None" requirement.
        """
        super().clean()
        # If user is a Reader, they cannot have a publisher
        if self.user_role == 'Reader':
            self.publisher_affiliation = None

    def __str__(self):
        """Returns the username."""
        return self.username

class Article(models.Model):
    """
    Represents a news article written by a Journalist.
    Requires Editor approval.
    """
    article_title = models.CharField(max_length=255)
    article_content = models.TextField()
    
    # Author must be a CustomUser (Journalist)
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='independent_articles'
    )
    
    # Requirement: Indicate editor approval
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        """Returns the article title."""
        return self.article_title

class Newsletter(models.Model):
    """
    Represents a newsletter published by a Journalist.
    """
    newsletter_title = models.CharField(max_length=255)
    newsletter_content = models.TextField()
    
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='independent_newsletters'
    )

    def __str__(self):
        """Returns the newsletter title."""
        return self.newsletter_title