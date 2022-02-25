from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from articles.views import *

urlpatterns = [
    path('', article_main),
]
