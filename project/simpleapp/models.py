from django.db import models
from django.core.validators import MinValueValidator


# Товар для нашей витрины
class News(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True, # названия товаров не должны повторяться
    )
    description = models.TextField()
    date = models.DateField()
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news', # все продукты в категории будут доступны через поле news
    )

    def __str__(self):
        return f'{self.description}'

    class Meta:
        verbose_name_plural = "News"




# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name_plural = "Categories"
