from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post


@receiver(post_save, sender=Post)
def reply_topic(sender, instance, **kwargs):
    email = instance.topic.starter.email
    topic_name = instance.topic.subject
    send_mail("Response on Topic", f"You received a reply to the topic '{topic_name}'\nResponse: {instance} ",
              'kd0996253125@gmail.com', [email], fail_silently=False)
