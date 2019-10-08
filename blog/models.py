from django.db import models
from django.contrib.auth.models import User

class BlogType(models.Model):
    type_name = models.CharField(max_length=15, verbose_name='博客分类')

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'<博客分类:{self.type_name}>'

class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    last_update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE,verbose_name='博客分类')
    is_delete = models.BooleanField(default=False, verbose_name='删除')

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return f'<博客:{self.title}>'