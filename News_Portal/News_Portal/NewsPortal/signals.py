from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import Post, Category
from .tasks import notify_on_creation

post_created: Post

@receiver(post_save, sender=Post)
def save_state(sender, instance, created, **kwargs):
    global post_created
    if created:
        post_created = instance
    else:
        post_created = None

@receiver(m2m_changed, sender=Post.categories.through)
def notify_users(sender, instance, action, **kwargs):
    global post_created
    if post_created != None and  action == 'post_add' and post_created.pk == instance.pk:
        print('Необходимо оповещение')
        notify_on_creation.delay(instance.pk) #.apply_async([instance.pk], countdown = 30)
        print('В очередь встали')
        post_created == None