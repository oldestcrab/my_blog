from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import  GenericForeignKey
from django.contrib.auth.models import User

class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    like_num = models.IntegerField(default=0, verbose_name='点赞量')

    class Meta:
        verbose_name = '点赞统计'
        verbose_name_plural = verbose_name


class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    liked_time = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='点赞用户')

    class Meta:
        verbose_name = '点赞记录'
        verbose_name_plural = verbose_name