from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


# Cтатьи для нашей витрины
class Articles(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,  # названия статей не должны повторяться
    )
    description = models.TextField()
    date = models.DateField(help_text=("YYYY-MM-DD"))

    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to="Category",
        on_delete=models.CASCADE,
        related_name="articles",  # все продукты в категории будут доступны через поле articles
    )

    def __str__(self):
        return f"{self.description}"

    def get_absolute_url(self):
        return reverse("articles_detail", args=[str(self.id)])

    class Meta:
        verbose_name_plural = "Articles"


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name_plural = "Categories"
