from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import Post, Category
from datetime import *
from celery import shared_task

@shared_task()
def send_week_posts():
    user: User
    old_date = datetime.today().date() - timedelta(7)
    #print ('прошлая дата', old_date)
    for user in User.objects.all():
        p = Post.objects.filter(categories__subscribers=user, date_added__date__gte=old_date)
        if p.count()!=0:
            html_content = render_to_string('eml_weekly_notification.html', {'post': p, 'user': user})
            send_mail('Новости за минувшую неделю', '', None, [user.email], html_message=html_content)

#для опробования
#@shared_task()
def test_email():
    user: User
    for user in User.objects.all():
        p = Post.objects.filter(categories__subscribers=user)
        if p.count()!=0:
            html_content = render_to_string('eml_weekly_notification.html', {'post': p, 'user': user})
            send_mail('Новости за минувшую неделю', '', None, [user.email], html_message=html_content)



@shared_task()
def notify_on_creation(id):
    print('вошли в notify')
    recipients = []
    sub: User
    cat: Category
    post: Post = Post.objects.get(pk=id)
    # print(post.cateChannelPromise' object has no attribute '__value__gories.all().count())
    for cat in post.categories.all():
        for sub in cat.subscribers.all():
            if not sub.email in recipients:
                recipients.append(sub.email)
                html_content = render_to_string('eml_post_created.html', {'post': post, 'user': sub})
                send_mail(f'{post.title}', '', None, [sub.email], html_message=html_content)
