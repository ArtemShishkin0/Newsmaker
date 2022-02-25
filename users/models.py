from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_delete
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

# class ImageQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         print(self)
#         for obj in self:
#             print(obj)
#             storage = obj.photo.storage
#             if storage.exists(obj.photo.name):
#                 storage.delete(obj.photo.name)
#             obj.photo.delete()
#             obj.img.delete()
#         super(ImageQuerySet, self).delete(*args, **kwargs)

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
        return str(self.name)

    def delete(self, using=None, keep_parents=False):
        storage = self.photo.storage
        if storage.exists(self.photo.name):
            storage.delete(self.photo.name)
        super().delete()

# @receiver(post_delete, sender=Info)
# def delete_image_hook(sender, instance, using, **kwargs):
#     print(instance)
#     instance.photo.delete()

admin.site.register(Info)



