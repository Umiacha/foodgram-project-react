# Generated by Django 3.2 on 2024-03-14 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0008_auto_20240313_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='in_favorited',
            field=models.ManyToManyField(related_name='favorited', through='recipes.Favorite', to=settings.AUTH_USER_MODEL, verbose_name='В избранном'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='in_shopping_cart',
            field=models.ManyToManyField(related_name='purchase', through='recipes.ShoppingCart', to=settings.AUTH_USER_MODEL, verbose_name='В корзине'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipe', to='recipes.Tag', verbose_name='Теги'),
        ),
    ]
