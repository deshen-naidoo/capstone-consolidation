"""
Admin configuration for the News application.
Registers models to make them manageable via the Django admin interface.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Publisher, CustomUser, Article, Newsletter

class CustomUserAdmin(UserAdmin):
    """
    Extends the default UserAdmin to display custom fields 
    in the Django admin panel.
    """
    # Adds our custom fields to the existing admin layout
    custom_fieldsets = (
        ('Custom Roles & Affiliations', {
            'fields': (
                'user_role', 
                'publisher_affiliation', 
                'subscribed_publishers', 
                'subscribed_journalists'
            ),
        }),
    )
    fieldsets = UserAdmin.fieldsets + custom_fieldsets

admin.site.register(Publisher)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Article)
admin.site.register(Newsletter)