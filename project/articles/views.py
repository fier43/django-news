from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
from .forms import ArticlesForm
from django.urls import reverse_lazy



# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
# from django.views.generic.detail import DetailView
from .models import Articles
from .filters import ArticlesFilter


class ArticlesList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Articles
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'title'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'articles.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'articles'
    paginate_by = 10 # вот так мы можем указать количество записей на странице

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        context['next_sale'] = f"Статей на текущее время:"

        return context

class ArticlesDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Articles
    # Используем другой шаблон — Articles.html
    template_name = 'articles-detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'articles'

class ArticlesSearch(ListView):
    model = Articles
    template_name = 'articles-search.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ArticlesFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        # context['time_now'] = datetime.utcnow()
        # # Добавим ещё одну пустую переменную,
        # # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['filterset'] = self.filterset

        return context

# Добавляем новое представление для создания товаров.
class ArticleCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = ArticlesForm
    # модель товаров
    model = Articles
    # и новый шаблон, в котором используется форма.
    template_name = 'articles-edit.html'

# Добавляем представление для изменения товара.
class ArticleUpdate(UpdateView):
    form_class = ArticlesForm
    model = Articles
    template_name = 'articles-edit.html'

# Представление удаляющее товар.
class ArticleDelete(DeleteView):
    model = Articles
    template_name = 'Articles-delete.html'
    success_url = reverse_lazy('articles_list')
