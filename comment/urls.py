from django.urls import path

from . import views

app_name = 'comment'

urlpatterns = [
    path('comment_update', views.comment_update, name='comment_update'),
]