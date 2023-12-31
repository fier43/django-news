# Generated by Django 4.2.3 on 2023-08-28 11:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simpleapp', '0004_remove_news_category_news_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='categories', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='news',
            name='category',
            field=models.ManyToManyField(related_name='news', to='simpleapp.category'),
        ),
    ]
