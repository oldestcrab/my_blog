from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def send_notification(sender, instance, **kwargs):
    """
    注册发送通知
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    # 判断是否是注册操作
    if kwargs['created'] == True:
        admin = User.objects.get(pk=1)

        # 系统通知
        verb_res = '恭喜注册成功，请继续探索吧~'
        # 用于查询分类
        type_res = 'resmsg'
        notify.send(admin, recipient=instance, verb=verb_res, target=instance, public=False,
                    action_object=admin, type=type_res)

        # 站内公告
        verb_sys = '请遵守协议，不要干坏事哦~'
        # 用于查询分类
        type_sys = 'sysmsg'
        notify.send(admin, recipient=instance, verb=verb_sys, target=instance, public=True,
                    action_object=admin, type=type_sys)