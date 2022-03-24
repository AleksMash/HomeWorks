from django.forms import ModelForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['author', 'post_type', 'title', 'categories', 'text']
    def save(self, commit=True):
        post = super().save()
        recipients = []
        sub: User
        for cat in post.categories.all():
            for sub in cat.subscribers.all():
                if not sub.email in recipients:
                    recipients.append(sub.email)
                    html_content = render_to_string('eml_post_created.html', {'post': post, 'user':sub})
                    msg = EmailMultiAlternatives(
                        subject=f'{post.title}',
                        from_email='amashukov@yandex.ru',
                        to=[sub.email],
                    )
                    msg.attach_alternative(html_content,"text/html")
                    msg.send()
        return post

class UpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'post_type', 'title', 'categories', 'text']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user