from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import Post, Category

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
        recipients = []
        sub: User
        #print(post.categories.all().count())
        for cat in instance.categories.all():
           for sub in cat.subscribers.all():
                if not sub.email in recipients:
                    recipients.append(sub.email)
                    html_content = render_to_string('eml_post_created.html', {'post': instance, 'user': sub})
                    send_mail(f'{instance.title}','',None,[sub.email],html_message=html_content)
        post_created == None