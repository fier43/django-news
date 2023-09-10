from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsSearch, NewsCreateView, NewUpdate, NewDelete, CategoryView, subscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60)(NewsList.as_view()), name='news_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>',NewsDetail.as_view(), name='news_detail'),
   path('search/', NewsSearch.as_view(), name='news_search'),
   path('create/', NewsCreateView.as_view(), name='news_create'),
   path('<int:pk>/update/', NewUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewDelete.as_view(), name='news_delete'),
   path('categories/<int:pk>', CategoryView.as_view(), name='category_details'),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),

]
