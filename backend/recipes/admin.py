from django.contrib.admin import ModelAdmin, register

from .models import Ingredient


@register(Ingredient)
class IngredientsAdmin(ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_filter = ['name']
