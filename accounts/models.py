from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # 关联自带的用户模型
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # nickname = models.CharField(max_length=20, blank=True, verbose_name='昵称')

    avatar = models.ImageField(upload_to='avatar/%Y-%m-%d', blank=True, verbose_name='头像')

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
def get_avatar_url(self):
    """
    获取用户头像
    :param self:
    :return: 用户头像或者默认头像
    """
    # 判断是否存在对象
    if Profile.objects.filter(user=self).exists():
        # 用户是否上传头像
        if Profile.objects.get(user=self).avatar:
            # 返回头像url
            return Profile.objects.get(user=self).avatar.url
    # 返回默认头像url
    return '/media/avatar/default_avatar.jpg'

# 动态绑定
User.get_avatar_url = get_avatar_url