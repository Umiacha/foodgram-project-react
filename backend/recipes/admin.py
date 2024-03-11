from django.contrib.admin import ModelAdmin, register, display

from .models import Ingredient, Tag, Recipe, Favorite


@register(Ingredient)
class IngredientsAdmin(ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_filter = ['name']


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['name', 'color', 'slug']


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    # TODO: Добавить отображение ингредиентов на основе RecipeIngredient. Создание рецепта в админке -- через ModelForm.
    list_display = ['name', 'get_username']
    list_filter = ['author', 'name', 'tags']
    readonly_fields = ['in_Favorite']

    def in_Favorite(self, obj):
        return obj.in_Favorite()
    
    @display(ordering='author__username', description='Author')
    def get_username(self, obj):
        return obj.author.username
