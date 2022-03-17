from django.urls import path, include
from articles.views import article_list,article_detail, article_create, article_publish, profiles_list, profile_detail, article_publish_list
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('articles/', article_list.as_view()),
    path('articles/create/', article_create.as_view()),
    path('articles/<int:pk>', article_detail.as_view()),
    path('publish/<int:pk>', article_publish.as_view()),
    path('profiles/', profiles_list.as_view()),
    path('profiles/<int:pk>', profile_detail.as_view()),
    path('publish/', article_publish_list.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
