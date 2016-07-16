from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
        author = models.ForeignKey('auth.User')
        title = models.CharField(max_length=200)
        text = models.TextField()
        created_date = models.DateTimeField(default=timezone.now)
        published_date = models.DateTimeField(blank=True, null=True)

        def publish(self):
            self.published_date = timezone.now()
            self.save()

        def __str__(self):
            return self.title

class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        email = models.EmailField()
        avatar = models.ImageField()
        last_ip = models.GenericIPAddressField()
        current_ip = models.GenericIPAddressField()
        character_name = models.CharField(max_length=25)
        


