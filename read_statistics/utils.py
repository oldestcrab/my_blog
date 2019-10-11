from django.contrib.contenttypes.models import ContentType

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

        readnumdetail, create = ReadNumDetail.objects.get_or_create(content_type=content_type, object_id=obj.pk)
        readnumdetail.read_num +=1
        readnumdetail.save()

    return key