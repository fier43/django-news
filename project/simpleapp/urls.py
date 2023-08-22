from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsSearch, NewCreate, NewUpdate, NewDelete, CategoryListView, subscribe


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', NewsList.as_view(), name='news_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('search/', NewsSearch.as_view(), name='news_search'),
   path('create/', NewCreate.as_view(), name='news_create'),
   path('<int:pk>/update/', NewUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewDelete.as_view(), name='news_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),

]
