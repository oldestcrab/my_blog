from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from notifications.signals import notify

from .models import LikeRecord

@receiver(post_save, sender=LikeRecord)
def send_notifications(sender, instance, **kwargs):
    """
    点赞发送通知
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if instance.content_type.model == 'blog':
        verb = f'{instance.user}点赞了你的博客{instance.content_object.title}'
    elif instance.content_type.model == 'comment':
        verb = f'{instance.user}点赞了你的回复{strip_tags(instance.content_object.content[:240])}'
    else:
        verb = ''
    notify.send(instance.user, recipient=instance.content_object.get_user(),
                verb=verb, target=instance.content_object,
                action_object=instance, url=instance.content_object.get_url())

