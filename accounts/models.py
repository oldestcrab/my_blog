from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # 关联自带的用户模型
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # nickname = models.CharField(max_length=20, verbose_name='昵称')

    def __str__(self):
        return f'<Profile: for {self.user}>'

'''
def get_nickname_or_username(self):
    """
    获取昵称或者用户名
    :param self:
    :return:昵称或者用户名
    """
    if Profile.objects.filter(user=self).exists():
        return Profile.objects.get(user=self).nickname
    else:
        return self.username

# 动态绑定
User.get_nickname_or_username = get_nickname_or_username
'''