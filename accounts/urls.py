from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('result', views.result, name='result'),
    path('user_info', views.user_info, name='user_info'),
    # path('change_nickname', views.change_nickname, name='change_nickname'),
    path('change_email', views.change_email, name='change_email'),
    path('active_email', views.active_email, name='active_email'),
    path('change_password', views.change_password, name='change_password'),
    path('sent_email_reset_password', views.sent_email_reset_password, name='sent_email_reset_password'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('change_avatar', views.change_avatar, name='change_avatar'),
]
