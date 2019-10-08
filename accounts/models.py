from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # 关联自带的用户模型
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, verbose_name='昵称')

    def __str__(self):
        return f'<Profile:{self.nickname} for {self.user}>'

