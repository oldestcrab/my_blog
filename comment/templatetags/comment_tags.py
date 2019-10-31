from django import template
from django.contrib.contenttypes.models import ContentType

from ..forms import CommentForm
from ..models import Comment

register = template.Library()

@register.simple_tag()
def get_comment_form(obj):
    """
    初始化评论表单
    :param obj: 模型对象
    :return: 初始化评论表单
    """
    content_type = ContentType.objects.get_for_model(obj).model
    form = CommentForm(initial={
        'content_type': content_type,
        'object_id': obj.pk,
        'reply_comment_id': 0,
    })
    return form

@register.simple_tag()
def get_comment_list(obj):
    """
    获取顶级评论列表
    :param obj: 模型对象
    :return: 顶级评论列表
    """
    content_type = ContentType.objects.get_for_model(obj)
    # 获取顶级评论
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')

@register.simple_tag()
def get_comment_count(obj):
    """
    评论数量统计
    :param obj: 模型对象
    :return: 评论数量统计
    """
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()

@register.simple_tag()
def get_comment_count_by_str(obj_str, pk):
    """
    通过模型的字符串名称以及具体模型ID获取评论数量统计
    :param obj_str: 模型的字符串名称
    :param pk: 具体模型ID
    :return: 具体模型的评论统计
    """
    content_type = ContentType.objects.get(model=obj_str)
    return Comment.objects.filter(content_type=content_type, object_id=pk).count()
