from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
import datetime

from .models import ReadNum, ReadNumDetail

def read_statistics_once_read(request, obj):
    """
    判断是否需要阅读量+1
    :param request: request
    :param obj: 模型对象
    :return: request cookies key,用于判断是否需要阅读量+1
    """
    content_type = ContentType.objects.get_for_model(obj)
    # 设置cookies key
    key = f'{content_type.model}_{obj.pk}_read'
    # 如果当前cookies没有该key,阅读数+1
    if not request.COOKIES.get(key):
        readnum, create = ReadNum.objects.get_or_create(content_type=content_type, object_id=obj.pk)
        readnum.read_num +=1
        readnum.save()

        # 当前时间
        date = timezone.now().date()
        readnumdetail, create = ReadNumDetail.objects.get_or_create(content_type=content_type, object_id=obj.pk, date=date)
        readnumdetail.read_num +=1
        readnumdetail.save()

    return key

def get_seven_days_read_data(content_type):
    """
    获取某个模型前一周的阅读量
    :param content_type: content_type
    :return: 前一周对应日期以及对应的改天总阅读量
    """
    # 今日日期
    today = timezone.now().date()

    days = []
    read_nums = []

    # 获取一周阅读量
    for i in range(6,-1,-1):
        day = today - datetime.timedelta(i)
        # 保存日期
        days.append(day.strftime('%m-%d'))
        # 获取某天的相关模型总阅读量
        result_detail = ReadNumDetail.objects.filter(content_type= content_type, date=day)
        result = result_detail.aggregate(read_count=Sum('read_num'))
        read_nums.append(result['read_count'] or 0)

    return days, read_nums

