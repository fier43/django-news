from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name="categories")

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name_plural = "Categories"


# Новость для нашей витрины
class News(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,  # названия товаров не должны повторяться
    )
    description = models.TextField()
    date = models.DateField(help_text=("YYYY-MM-DD"))

    # поле категории будет ссылаться на модель категории
    category = models.ManyToManyField(
        Category,
        related_name="news",  # все новости в категории будут доступны через поле news
    )

    def __str__(self):
        return f"{self.description}"

    def get_absolute_url(self):
        return reverse("news_detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(
            *args, **kwargs
        )  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(
            f"product-{self.pk}"
        )  # затем удаляем его из кэша, чтобы сбросить его

    def preview(self):
        return f"{self.description[:124]}..."

    class Meta:
        verbose_name_plural = "News"
