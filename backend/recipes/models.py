from django.contrib.admin import display
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=200, verbose_name='Единицы измерения'
    )
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название', unique=True
    )
    color = models.CharField(
        max_length=7, verbose_name='Цвет', unique=True
    )
    slug = models.SlugField(
        max_length=200, verbose_name='Слаг', unique=True, validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )
    
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
    
    def __str__(self):
        return f'{self.name} {self.slug}'


class Recipe(models.Model):
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', through_fields=('recipe', 'ingredient'), verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')  # Maybe it needs to add through=RecipeTag ??
    image = models.ImageField(verbose_name='Картинка')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор публикации')
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(validators=[MinValueValidator(limit_value=1)], verbose_name='Время приготовления (в минутах)')
    
    @display(description='in_Favorite')
    def in_Favorite(self):
        """Count how many users add recipe in Favorite."""
        return Favorite.objects.filter(recipe=self).count()
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    
    def __str__(self):
        return f'Рецепт {self.name}.'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    amount = models.PositiveIntegerField(verbose_name='Количество')
    
    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
    
    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite_user_recipe')
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
