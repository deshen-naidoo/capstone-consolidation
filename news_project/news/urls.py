"""
URL configurations for the news application.
"""
from django.urls import path
from . import views

urlpatterns =[
    # Web Routes
    path('', views.home_dashboard, name='home_dashboard'),
    path('editor/', views.editor_dashboard, name='editor_dashboard'),
    path(
        'editor/approve/<int:article_id>/', 
        views.approve_article, 
        name='approve_article'
    ),
    
    # API Routes
    path('api/my-feed/', views.api_subscription_feed, name='api_feed'),
]