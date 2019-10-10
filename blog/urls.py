from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('blog_with_type/<int:blog_type_pk>', views.blog_with_type, name='blog_with_type'),
]