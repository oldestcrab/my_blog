from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField

from read_statistics.models import ReadNumExpandMethod, ReadNumDetail

class BlogType(models.Model):
    type_name = models.CharField(max_length=15, verbose_name='博客分类')

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name

class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50, verbose_name='标题')
    content = RichTextUploadingField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    last_update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE,verbose_name='博客分类')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    # # 反向关联模型，产生对应关系，不会产生字段
    read_num_details = GenericRelation(ReadNumDetail)

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return f'<博客:{self.title}>'

    def get_user(self):
        return self.author

    def get_url(self):
        return reverse('blog:blog_detail', kwargs={'blog_pk':self.pk})