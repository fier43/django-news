from django.urls import path

# Импортируем созданное нами представление
from .views import (
    ArticlesList,
    ArticleDelete,
    ArticlesSearch,
    ArticleCreate,
    ArticleUpdate,
    ArticlesDetail,
)


urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path("", ArticlesList.as_view(), name="articles_list"),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path("<int:pk>", ArticlesDetail.as_view(), name="articles_detail"),
    path("search-art/", ArticlesSearch.as_view(), name="articles_search"),
    path("create-art/", ArticleCreate.as_view(), name="articles_create"),
    path("<int:pk>/update-art/", ArticleUpdate.as_view(), name="articles_update"),
    path("<int:pk>/delete-art/", ArticleDelete.as_view(), name="articles_delete"),
]
