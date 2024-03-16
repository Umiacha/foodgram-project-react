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
    in_favorited = models.ManyToManyField(User, through='Favorite', through_fields=('recipe', 'user'), verbose_name='В избранном', related_name='favorited')
    in_shopping_cart = models.ManyToManyField(User, through='ShoppingCart', through_fields=('recipe', 'user'), verbose_name='В корзине', related_name='purchase')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', related_name='recipe')  # Maybe it needs to add through=RecipeTag ??
    image = models.ImageField(upload_to='recipes/images/', verbose_name='Картинка')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe', verbose_name='Автор публикации')
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


class ShoppingCart(models.Model):
    """Recipes that users add in their carts.
    
    Suggested that user can add recipe only ONCE (pair (user, recipe) is unique)!"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='В корзине')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'), name='unique_user_recipe')
        ]
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
