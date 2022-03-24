from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # импортируем класс
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.views import View  # импортируем простую вьюшку
from .models import Post, Category
from .filters import NewsFilter
from .forms import PostForm, UpdateForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


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
    #queryset = Post.objects.all.order_by('-id')
    ordering = ['-id']
    paginate_by = 2  #выводим по 3 новостей на страницу

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


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

class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post')
    template_name = 'post_create.html'
    form_class = PostForm

class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post')
    template_name = 'post_create.html'
    form_class = UpdateForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPortal.delete_post')
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

@login_required
def be_author(request):
    user = request.user
    auth_group:Group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        auth_group.user_set.add(user)
    return redirect('/')

#подписка на новости определенной категории
@login_required
def cat_subscribe(request, cat_id):
    user = request.user
    cat = Category.objects.get(pk=cat_id)
    cat.subscribers.add(user)
    context = {'cat':cat}
    return render(request, "subscribe_for_category.html",context=context)

class CategoryView(ListView):
    model = Post
    template_name = 'news_from_category.html'
    context_object_name = 'news'
    ordering = ['-date_added']

    def get_context_data(self, **kwargs):  #забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        cat = Category.objects.get(pk=id)
        context['cat_name'] = cat.name
        context['cat_id'] = cat.id
        context['news']=Post.objects.filter(categories=cat)
        return context