"""
Automated unit tests for the News API.
Checks subscription filtering and access control.
"""
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser, Article, Publisher

class APIFeedTest(APITestCase):
    """
    Tests the REST API feed to ensure users only see 
    approved articles from their active subscriptions.
    """
    
    def setUp(self):
        """Sets up the database with dummy users and articles."""
        self.journalist_1 = CustomUser.objects.create_user(
            username="j1", password="password", user_role="Journalist"
        )
        
        self.journalist_2 = CustomUser.objects.create_user(
            username="j2", password="password", user_role="Journalist"
        )
        
        self.reader = CustomUser.objects.create_user(
            username="reader", password="password", user_role="Reader"
        )
        
        # Subscribe the reader ONLY to journalist 1
        self.reader.subscribed_journalists.add(self.journalist_1)
        
        # Create an approved article by journalist 1 (Should appear)
        self.article_1 = Article.objects.create(
            article_title="J1 Approved News",
            article_content="Content here.",
            author=self.journalist_1,
            is_approved=True
        )
        
        # Create an approved article by journalist 2 (Should NOT appear)
        self.article_2 = Article.objects.create(
            article_title="J2 Approved News",
            article_content="Content here.",
            author=self.journalist_2,
            is_approved=True
        )
        
        # Create an UNAPPROVED article by journalist 1 (Should NOT appear)
        self.article_3 = Article.objects.create(
            article_title="J1 Unapproved News",
            article_content="Content here.",
            author=self.journalist_1,
            is_approved=False
        )

    def test_feed_returns_only_subscribed_approved_articles(self):
        """
        Ensures the API filters out unapproved articles and 
        articles from unsubscribed authors.
        """
        # FIX: Use DRF's force_authenticate to bypass the 401 error
        self.client.force_authenticate(user=self.reader)
        
        api_url = reverse("api_feed")
        response = self.client.get(api_url)
        
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        
        # The reader should only see article_1
        self.assertEqual(len(response_data), 1)
        self.assertEqual(
            response_data[0]["article_title"], 
            "J1 Approved News"
        )

    def test_feed_requires_authentication(self):
        """
        Robustness Test: Ensures unauthenticated users cannot access feed.
        """
        api_url = reverse("api_feed")
        response = self.client.get(api_url)
        
        # 401 Unauthorized is the expected REST response
        self.assertEqual(response.status_code, 401)