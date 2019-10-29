from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from notifications.signals import notify

from .models import Comment

@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    """
    评论发送通知
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    # 判断评论的是博客还是评论
    if instance.reply_to:
        recipient = instance.reply_to
        verb = f'{instance.user}回复了你的评论{strip_tags(instance.content[:240])}'
    else:
        recipient = instance.content_object.get_user()
        # 判断是否为博客
        if instance.content_type.model == 'blog':
            verb = f'{instance.user}评论了你的博客{instance.content_object.title}'
        else:
            raise Exception('unknown comment object type')
    # 添加锚点，方便前端定位
    url = instance.get_url() + '#comment_' + str(instance.pk)
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance,
           target=instance, url=url)