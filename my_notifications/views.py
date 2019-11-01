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
    # 判断用户是否登录
    if not request.user.is_authenticated:
        raise Http404

    type = request.GET.get('type', 'comment')

    # 获取消息列表
    # 评论
    """
    if type == 'comment':
        notification_list = Notification.objects.filter(recipient=request.user,
                                                        action_object_content_type=ContentType.objects.get(model=type))
    # 点赞
    elif type == 'likes':
        notification_list = Notification.objects.filter(recipient=request.user,
                                                        action_object_content_type=ContentType.objects.get(model='likerecord'))
    # 系统通知
    elif type == 'resmsg':
        # admin = User.objects.get(pk=1)
        content_type = ContentType.objects.get(model='user')
        notification_list = Notification.objects.filter(actor_content_type=content_type, actor_object_id=1, recipient=request.user, public=False)

    # 站内公告
    elif type == 'sysmsg':
        # admin = User.objects.get(pk=1)
        content_type = ContentType.objects.get(model='user')
        notification_list = Notification.objects.filter(actor_content_type=content_type, actor_object_id=1, recipient=request.user, public=True)
    else:
        raise Http404
    """
    if type == 'comment' or type == 'likes' or type == 'resmsg' or type == 'sysmsg':
        notification_list = Notification.objects.filter(recipient=request.user, data__contains=f'"type":"{type}"')
        # 标记为已读
        notification_list.mark_all_as_read()
    else:
        raise Http404
    # 分页
    current_page, range_page = common_paginator(request, notification_list, 10)

    context = {
        'current_page': current_page,
        'range_page': range_page,
        'paginator_kw' : f'type={type}&',
        'type': type,
    }
    return render(request, 'my_notifications/my_notifications.html', context=context)