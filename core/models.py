from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    file_url = models.URLField(max_length=200)
    upload_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expiry_date

    def __str__(self):
        return self.title