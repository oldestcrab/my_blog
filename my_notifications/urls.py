from django.urls import path

from . import views

app_name = 'my_notifications'

urlpatterns = [
    path('', views.my_notifications, name='my_notifications'),
]