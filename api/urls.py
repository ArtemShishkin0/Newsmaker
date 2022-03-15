from django.urls import path, include
from articles.views import article_list,article_detail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('articles/', article_list.as_view()),
    path('articles/<int:pk>', article_detail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
