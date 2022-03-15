from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from NewsMaker.views import login_view
from articles.views import *
from ajax.views import *
from users.views import *
from articles.views import article_main
urlpatterns = [
    path('validate_data', validate_data, name="validate_data"),
    path('article_main', article_main, name="article_main"),
    path('register_validation', register, name='register_validation'),
    path('login_check', login_view, name='login_check'),
    path('password_update', profile, name='password_update'),
]
