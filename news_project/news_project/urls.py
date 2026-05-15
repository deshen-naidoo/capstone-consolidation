"""
Main project URLs for the News Application.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns =[
    path('admin/', admin.site.urls),
    # Links the root path directly to the news app
    path('', include('news.urls')),
]