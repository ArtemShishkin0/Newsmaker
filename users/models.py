import os

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.dispatch import receiver
from django.db.models.signals import post_delete
from phonenumber_field.modelfields import PhoneNumberField

class Info(models.Model):
    #object = ImageQuerySet.as_manager()
    name = models.OneToOneField(User, max_length=200, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    about = models.CharField(max_length=500, blank=True)
    photo = models.ImageField(blank=True, upload_to='userimages/')
    phone = PhoneNumberField(blank=True, unique=True, null=True)
    show_email = models.BooleanField(default=True)
    show_phone = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name).capitalize()

admin.site.register(Info)

@receiver(post_delete, sender=Info, dispatch_uid='info_delete_signal')
def delete_clean(sender, instance, using, **kwargs):
    try:
        os.remove(instance.photo.path)
    except Exception as err:
        print(err)
