from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

from .models import LikeRecord

@receiver(post_save, sender=LikeRecord)
def send_notification(sender, instance, **kwargs):
    """
    点赞发送通知
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if instance.content_type.model == 'blog':
        verb = f'点赞了你的文章'
        description = f'<a href="{instance.content_object.get_url()}" target="_blank">《{instance.content_object.title}》</a>'
        url = instance.content_object.get_url()
    elif instance.content_type.model == 'comment':
        verb = f'点赞了你在文章<a href="{instance.content_object.get_url()}" target="_blank">《{instance.content_object.content_object.title}》</a>中的回复'
        url = instance.content_object.get_url() + '#comment_' + str(instance.content_object.pk)
        description = f'<a href="{url}" target="_blank">{instance.content_object.content}</a>'
    else:
        return
    # 添加锚点，方便前端定位
    notify.send(instance.user, recipient=instance.content_object.get_user(),
                verb=verb, description=description, target=instance.content_object,
                action_object=instance, url=url)

