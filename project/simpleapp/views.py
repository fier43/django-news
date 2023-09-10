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
from .models import News, Category
from .filters import NewsFilter
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.core.mail import send_mail
from django.core.cache import cache

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
    template_name = 'news/news-detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news'

    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'news-{self.kwargs["pk"]}', None) # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)
            return obj

class NewsSearch(ListView):
    model = News
    template_name = 'news/search.html'
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
class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_news')
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель товаров
    model = News
    # и новый шаблон, в котором используется форма.
    template_name = 'news/new_edit.html'

# Добавляем представление для изменения товара.
class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ( 'simpleapp.change_news')
    form_class = NewsForm
    model = News
    template_name = 'news/new_edit.html'

# Представление удаляющее товар.
class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_news')
    model = News
    template_name = 'news/new_delete.html'
    success_url = reverse_lazy('news_list')


class CategoryView(NewsList):
    model = News
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = News.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категорий'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})
