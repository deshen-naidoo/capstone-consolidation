"""
Views for the News Application.
Handles the web dashboard and REST API endpoints.
"""
# --- Standard & Django Imports ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMessage

# --- DRF Imports (For API) ---
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# --- Local App Imports ---
from .models import Article, CustomUser
from .functions.tweet import Tweet
from .serializers import ArticleSerializer


# ==========================================
# WEB VIEWS (Dashboards & Editor Actions)
# ==========================================

def home_dashboard(request):
    """Serves as the root URL path. Displays approved articles."""
    approved_articles = Article.objects.filter(is_approved=True)
    context_data = {"articles": approved_articles}
    return render(request, "news/home.html", context_data)

def is_editor_check(user_account):
    """Validation function to check if a user is an Editor."""
    if not user_account.is_authenticated:
        return False
    return user_account.user_role == 'Editor'

@user_passes_test(is_editor_check, login_url='/admin/')
def editor_dashboard(request):
    """Displays unapproved articles for Editors to review."""
    unapproved_articles = Article.objects.filter(is_approved=False)
    context_data = {"pending_articles": unapproved_articles}
    return render(request, "news/editor_dashboard.html", context_data)

@user_passes_test(is_editor_check, login_url='/admin/')
def approve_article(request, article_id):
    """Approves an article and triggers email/tweet notifications."""
    if request.method == "POST":
        target_article = get_object_or_404(Article, pk=article_id)
        target_article.is_approved = True
        target_article.save()

        # Step 1: Send Email
        try:
            author = target_article.author
            subscribers = CustomUser.objects.filter(
                subscribed_journalists=author
            )
            
            subscriber_emails =[]
            for sub in subscribers:
                if sub.email:
                    subscriber_emails.append(sub.email)
            
            if len(subscriber_emails) > 0:
                email_sub = "New Article by " + author.username
                email_msg = "Read it now: " + target_article.article_title
                
                alert_email = EmailMessage(
                    email_sub, email_msg, "alerts@news.com", subscriber_emails
                )
                alert_email.send()
        except Exception as e:
            print("Email failed: " + str(e))

        # Step 2: Post to Twitter
        try:
            tweet_text = "Breaking News: " + target_article.article_title
            tweet_payload = {"text": tweet_text}
            Tweet().make_tweet(tweet_payload)
        except Exception as e:
            print("Tweet failed: " + str(e))

    return redirect('editor_dashboard')


# ==========================================
# REST API VIEWS
# ==========================================

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_subscription_feed(request):
    """
    RESTful API endpoint. Returns approved articles from 
    publishers and journalists the authenticated user is subscribed to.
    """
    try:
        current_user = request.user
        
        # Retrieve user's specific subscriptions
        subbed_journalists = current_user.subscribed_journalists.all()
        subbed_publishers = current_user.subscribed_publishers.all()
        
        # Filter 1: Approved articles by subscribed journalists
        journalist_articles = Article.objects.filter(
            is_approved=True,
            author__in=subbed_journalists
        )
        
        # Filter 2: Approved articles by subscribed publishers
        publisher_articles = Article.objects.filter(
            is_approved=True,
            author__publisher_affiliation__in=subbed_publishers
        )
        
        # Combine querysets and remove duplicates
        feed_articles = (journalist_articles | publisher_articles).distinct()
        
        # Serialize and return JSON response
        serializer = ArticleSerializer(feed_articles, many=True)
        return Response(serializer.data)
        
    except Exception as api_error:
        # Robustness: Anticipate unexpected database or user logic errors
        error_msg = {"error": "Failed to retrieve feed: " + str(api_error)}
        return Response(error_msg, status=500)