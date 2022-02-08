from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # импортируем класс
from django.views import View  # импортируем простую вьюшку
from .models import Post
from .filters import NewsFilter
from .forms import PostForm
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод

# который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
# Create your views here.

class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'     # указываем имя шаблона, в котором будет лежать _HTML_,
                                    # в котором будут все инструкции о том,
                                    # как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'    # это имя списка, в котором будут
                                    # лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через _HTML_-шаблон
    queryset = Post.objects.filter(post_type=2).order_by('-id')
    paginate_by = 2  #выводим по 3 новостей на страницу


# создаём представление, в котором будут детали конкретного отдельного товара
class NewDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'SingleNew.html'  # название шаблона будет SingleNew.html
    context_object_name = 'single_new'  # название объекта. в нём будет

class NewsFiltered(ListView):
    model = Post
    template_name = 'news_filtered.html'
    context_object_name = 'news'
    ordering = ['-date_added']

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['news'] = NewsFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

class PostCreateView(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm

class PostUpdateView(UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

