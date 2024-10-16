from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
