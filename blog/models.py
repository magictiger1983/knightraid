from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.

def upload_location(instance, filename):
    if instance.id:
        return "%s/%s" %(instance.id, filename)
    else:
        qs = Post.objects.all().order_by("-id")
        last_id = qs.first().id
        new_id = last_id + 1
        return "%s/%s" %(new_id, filename)

def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



class Post(models.Model):
        author = models.ForeignKey('auth.User')
        image = models.ImageField(upload_to=upload_location,null=True, blank=True, height_field='image_height', width_field='image_width')
        image_height = models.IntegerField(default=0)
        image_width = models.IntegerField(default=0)
        title = models.CharField(max_length=200)
        text = models.TextField()
        created_date = models.DateTimeField(default=timezone.now)
        published_date = models.DateTimeField(blank=True, null=True)
        slug = models.SlugField(unique=True)

        def publish(self):
            self.published_date = timezone.now()
            self.save()

        def __str__(self):
            return self.title

        def approved_comments(self):
            return self.comments.filter(approved_comment=True)


class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        email = models.EmailField()
        avatar = models.ImageField()
        last_ip = models.GenericIPAddressField()
        current_ip = models.GenericIPAddressField()
        character_name = models.CharField(max_length=25)
        

class Comment(models.Model):
        post = models.ForeignKey('blog.Post', related_name='comments')
        author = models.CharField(max_length=200)
        text = models.TextField()
        created_date = models.DateTimeField(default=timezone.now)
        approved_comment = models.BooleanField(default=False)

        def approve(self):
           self.approved_comment = True
           self.save()

        def __str__(self):
           return self.text

pre_save.connect(pre_save_post_receiver, sender=Post)