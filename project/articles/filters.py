from django.forms.widgets import TextInput
from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from .models import Category, Articles

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class ArticlesFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains', field_name='title', label='По названию')
    category = ModelChoiceFilter(queryset=Category.objects.all(), field_name='category', label='По категории')
    date__gt = DateFilter(field_name="date", lookup_expr='gt', label='Позже указываемой даты', widget=TextInput(attrs={'type': 'date'}))

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Articles
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = ['title', 'category', 'date__gt']

