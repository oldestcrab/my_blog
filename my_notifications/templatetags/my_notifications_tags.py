from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def my_notifications_unread(context, type):
    """
    获取相关消息类型的未读消息计数
    :param context:
    :param type: 消息类型
    :return: 相关消息类型的未读消息计数
    """
    user = context['user']
    # 先判断是否登录
    if not user.is_authenticated:
        return False
    # 返回相关消息类型的未读消息计数
    return user.notifications.unread().filter(data__contains=f'"type":"{type}"').count()