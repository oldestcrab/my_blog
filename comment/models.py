from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.urls import reverse

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='用户')

    # 顶级评论
    root = models.ForeignKey('self', on_delete=models.CASCADE, related_name='root_comment', null=True, verbose_name='顶级评论')
    # 父辈评论
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_comment', null=True, verbose_name='父辈评论')
    # 评论指向谁
    reply_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies', null=True, verbose_name='指向评论')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['comment_time']

    def get_user(self):
        return self.user

    def get_url(self):
        return self.content_object.get_url()