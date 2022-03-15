from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from uuid import uuid4
import os

import math

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

from ckeditor.widgets import CKEditorWidget

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("articleimages")

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    description = models.TextField(max_length=150)
    content = RichTextUploadingField(max_length=30000)
    created = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(blank=True, upload_to=path_and_rename)
    active = models.BooleanField(default=False)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.author} - {self.title} - {self.created.strftime('%d.%m.%Y %H:%M')}"

    def whenpublished(self):
        now = timezone.now()
        diff = now - self.created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


admin.site.register(Article)
admin.site.register(Category)

@receiver(post_delete, sender=Article, dispatch_uid='article_delete_signal')
def delete_clean(sender, instance, using, **kwargs):
    try:
        os.remove(instance.thumbnail.path)
    except Exception as err:
        print(err)
