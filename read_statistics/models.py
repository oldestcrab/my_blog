from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import  GenericForeignKey
from django.core.exceptions import ObjectDoesNotExist

class ReadNum(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    read_num = models.IntegerField(default=0, verbose_name='阅读量')

    class Meta:
        verbose_name = '阅读统计'
        verbose_name_plural = verbose_name

# 扩展一些方法，方便调用
class ReadNumExpandMethod():
    def get_read_num(self):
        """
        获取阅读量，无则返回0
        :return: 阅读量
        """
        try:
            content_type = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=content_type, object_id=self.pk)
            return readnum.read_num
        except ObjectDoesNotExist:
            return 0


class ReadNumDetail(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    read_num = models.IntegerField(default=0, verbose_name='阅读量')
    date = models.DateField(auto_now_add=True, verbose_name='日期')

    class Meta:
        verbose_name = '详细阅读统计'
        verbose_name_plural = verbose_name