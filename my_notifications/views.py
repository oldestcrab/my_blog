from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from notifications.models import Notification

def my_notifications(request):
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
    for i in notification_list:
        print(i.action_object_content_type)
        print(i.action_object_object_id)
        print(i.action_object)
    context = {
        'notification_list': notification_list,
    }
    return render(request, 'my_notifications/my_notifications.html', context=context)