import datetime

from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import Post, Category
from datetime import *


def send_week_posts():
    user: User
    old_date = datetime.today().date() - timedelta(7)
    #print ('прошлая дата', old_date)
    for user in User.objects.all():
        p = Post.objects.filter(categories__subscribers=user, date_added__date__gte=old_date)
        if p.count()!=0:
            html_content = render_to_string('eml_weekly_notification.html', {'post': p, 'user': user})
            send_mail('Новости за минувшую неделю', '', None, [user.email], html_message=html_content)
