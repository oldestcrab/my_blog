"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('likes/', include('likes.urls', namespace='likes')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('notifications/', include(notifications.urls, namespace='notifications')),
    path('my_notifications/', include('my_notifications.urls', namespace='my_notifications')),
    path('mdeditor/', include('mdeditor.urls')),

    path('', views.home, name='home'),
    path('search', views.search, name='search'),
]

# 开发环境中访问文件方法
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
