from django.db import models
from django.contrib import auth

class User(auth.models.User, auth.models.PermissionsMixin):
    """Custom user model extending Django's built-in user and permissions mixin."""
    
    def __str__(self):
        return self.username  # Changed from `self.name` to `self.username` to match the User model
