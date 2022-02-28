from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from uuid import uuid4
import os

import math
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
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("articleimages")
#postdelete
class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    description = models.TextField(max_length=150)
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(blank=True, upload_to=path_and_rename)
    OTHER = 'Other'
    TECHNOLOGIES = 'Technologies'
    NATURE = 'Nature'

    CATEGORIES = [
        (OTHER, 'Other'),
        (TECHNOLOGIES, "Technologies"),
        (NATURE, 'Nature')
    ]
    category = models.CharField(choices=CATEGORIES, default=OTHER, max_length=100)
    active = models.BooleanField(default=False)

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

    def delete(self, using=None, keep_parents=False):
        storage = self.thumbnail.storage
        if storage.exists(self.thumbnail.name):
            storage.delete(self.thumbnail.name)
        super().delete()

admin.site.register(Article)
