from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from articles.views import *
from ajax.views import *
urlpatterns = [
    path('validate_data', validate_data, name="validate_data"),
]
