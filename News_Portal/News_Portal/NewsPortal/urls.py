from django.urls import path
from .views import NewsList, NewDetail, NewsFiltered, PostCreateView, PostUpdateView, PostDeleteView  # импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    path('', NewsList.as_view()),
    # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', NewDetail.as_view(), name = 'singlenew'),  # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('search/',NewsFiltered.as_view()),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete')
]