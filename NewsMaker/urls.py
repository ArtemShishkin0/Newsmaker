from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from NewsMaker.views import *
from articles.views import *
from users.views import *
from django_email_verification import urls as email_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('login/', login_view),
    path('logout/', logout_view),
    path('home/', include('articles.urls')),
    path('email/', include(email_urls)),
    path('create/', create),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('home/article/<int:pk>', article_view),
    path('profile/<str:pk>/', profile),
    path('profile/', profile),
    path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('', RedirectView.as_view(url='home/', permanent=False)),
    path('ajax/', include('ajax.urls')),
    path('publishing/', include('publishing.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

