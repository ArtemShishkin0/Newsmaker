from django.urls import path, include
from publishing.views import *
urlpatterns = [
    path('', article_publish),
    path('article/<int:pk>', article_view_before_publish)
]