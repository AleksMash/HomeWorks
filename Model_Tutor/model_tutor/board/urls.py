from django.urls import path
from board.views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
]