from django.shortcuts import render
from django.views.generic import ListView, DetailView  # импортируем класс,
from .models import Post

# который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
# Create your views here.

class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'     # указываем имя шаблона, в котором будет лежать _HTML_,
                                    # в котором будут все инструкции о том,
                                    # как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'    # это имя списка, в котором будут
                                    # лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через _HTML_-шаблон


# создаём представление, в котором будут детали конкретного отдельного товара
class NewDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'SingleNew.html'  # название шаблона будет SingleNew.html
    context_object_name = 'single_new'  # название объекта. в нём будет