from django.urls import path
from .views import NewsList, NewDetail, NewsFiltered, PostCreateView, PostUpdateView,\
    PostDeleteView, be_author, CategoryView, cat_subscribe, test_view# импортируем наше представление
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    path('', NewsList.as_view()),
    # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', NewDetail.as_view(), name = 'singlenew'),  # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('search/',NewsFiltered.as_view()),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path ('login/', LoginView.as_view(template_name = 'login.html'), name='login'),
    path ('logout/', LogoutView.as_view(template_name = 'logout.html'), name='logout'),
    path ('be_author/', be_author, name = 'be_author'),
    path ('from_cat/<int:pk>', CategoryView.as_view(template_name = 'news_from_category.html'), name='cat_view'),
    path ('cat_subscribe/<int:cat_id>',cat_subscribe, name="cat_subscribe"),
    path ('command/<str:command>',test_view, name="command")
]