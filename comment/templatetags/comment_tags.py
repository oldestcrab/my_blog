from django import template
from django.contrib.contenttypes.models import ContentType

from ..forms import CommentForm

register = template.Library()

@register.simple_tag()
def get_comment_form(obj):
    """
    初始化评论表单
    :param obj: 模型对象
    :return:
    """
    content_type = ContentType.objects.get_for_model(obj).model
    form = CommentForm(initial={
        'content_type': content_type,
        'object_id': obj.pk,
        'reply_comment_id': 0,
    })
    return form
