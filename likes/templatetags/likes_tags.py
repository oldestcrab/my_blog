from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import LikeRecord, LikeCount

register = template.Library()

@register.simple_tag
def get_content_type(obj):
    """
    获取模型字符串
    :param obj: 模型对象
    :return: 模型字符串
    """
    # 通过ContentType获取对应模型字符串
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model

# 调用模板上下文
@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    """
    获取点赞状态
    :param context: context
    :param obj: 模型对象
    :return: 'active' or ''
    """
    user = context['user']
    # 先判断是否登录
    if not user.is_authenticated:
        return ''

    content_type = ContentType.objects.get_for_model(obj)
    # 判断数据是否存在
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
def get_like_num(obj):
    """
    获取点赞数
    :param obj: 模型对象
    :return: 点赞数
    """
    content_type = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)

    return like_count.like_num