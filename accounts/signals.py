from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def send_notifications(sender, instance, **kwargs):
    print(1)
    print(kwargs)
    if kwargs['created'] == True:
        admin = User.objects.get(pk=1)
        verb = '恭喜注册成功，请继续探索吧~'
        notify.send(admin, recipient=instance, verb=verb, target=instance,
                    action_object=instance, )
