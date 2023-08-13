from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
# from django.views.generic.detail import DetailView
from .models import News
from .filters import NewsFilter


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = News
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'title'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10 # вот так мы можем указать количество записей на странице

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        context['next_sale'] = f"Новостей на текущее время:"

        return context

class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = News
    # Используем другой шаблон — News.html
    template_name = 'news-detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news'

class NewsSearch(ListView):
    model = News
    template_name = 'search.html'
    context_object_name = 'news'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
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
class NewCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_news')
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель товаров
    model = News
    # и новый шаблон, в котором используется форма.
    template_name = 'new_edit.html'

# Добавляем представление для изменения товара.
class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ( 'simpleapp.change_news')
    form_class = NewsForm
    model = News
    template_name = 'new_edit.html'

# Представление удаляющее товар.
class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_news')
    model = News
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')
