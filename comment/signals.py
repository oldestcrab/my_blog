from django.db.models.signals import post_save
from django.dispatch import receiver
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
        verb = f'在文章<a href="{instance.get_url()}" target="_blank">《{instance.content_object.title}》</a>中回复了你'
        # 获取评论对象内容，如果有
        reply_to = instance.parent.content
    else:
        recipient = instance.content_object.get_user()
        # 判断是否为博客
        if instance.content_type.model == 'blog':
            verb = f'评论了你的文章<a href="{instance.get_url()}" target="_blank">《{instance.content_object.title}》</a>'
            reply_to = False
        else:
            raise Exception('unknown comment object type')

    # 添加锚点，方便前端定位
    url = instance.get_url() + '#comment_' + str(instance.pk)
    notify.send(instance.user, recipient=recipient, verb=verb, description=instance.content, action_object=instance,
           target=instance, url=url, reply_to=reply_to)