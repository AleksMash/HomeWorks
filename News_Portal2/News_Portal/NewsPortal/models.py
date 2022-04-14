from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache

# Create your models here.
class Author(models.Model):
    user_rate = models.FloatField(default = 0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rate(self, newrate):
        self.user_rate = newrate
        self.save()

    def __str__(self):
        return f'{self.user.username.title()}'



class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)
    subscribers = models.ManyToManyField(User)
    def __str__(self):
        return f'{self.name.title()}'

    def get_absolute_url(self):
        return reverse('cat_view', kwargs={'pk': self.pk})

    def get_url_for_mail(self):
        return "http://127.0.0.1:8000"+self.get_absolute_url()

class Post(models.Model):
    unknown = 0
    article = 1
    new = 2
    types = [(article, "Статья"), (new, "Новость")]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.IntegerField(choices=types, default=unknown)
    date_added = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    post_rate = models.FloatField(default=0.0)
    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        self.post_rate -= 1
        self.save()

    def preview(self):
        if len(self.text) < 124:
            return self.text
        else:
            return self.text[0:123] + '...'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def get_url_for_mail(self):
        return "http://127.0.0.1:8000"+self.get_absolute_url()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    comment_rate = models.FloatField(default=0.0)
    comment_text = models.TextField()

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()



