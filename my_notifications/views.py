from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from notifications.models import Notification

from my_blog.utils import common_paginator

def my_notifications(request):
    """
    消息页面视图
    :param request:
    :return:
    """
    type = request.GET.get('type', 'comment')
    # 评论
    if type == 'comment':
        action_object_content_type = ContentType.objects.get(model=type)
    # 点赞
    elif type == 'likes':
        action_object_content_type = ContentType.objects.get(model='likerecord')
    # 系统通知
    elif type == 'resmsg':
        action_object_content_type = ContentType.objects.get(model='user')
    else:
        raise Http404
    # 获取消息列表
    notification_list = Notification.objects.filter(recipient=request.user, action_object_content_type=action_object_content_type)
    # 分页
    current_page, range_page = common_paginator(request, notification_list, 7)

    context = {
        'current_page': current_page,
        'range_page': range_page,
        'paginator_kw' : f'type={type}&',
        'type': type,
    }
    return render(request, 'my_notifications/my_notifications.html', context=context)