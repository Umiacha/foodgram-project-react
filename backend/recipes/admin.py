from django.contrib.admin import ModelAdmin, register

from .models import Ingredient, Tag


@register(Ingredient)
class IngredientsAdmin(ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_filter = ['name']


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['name', 'color', 'slug']
