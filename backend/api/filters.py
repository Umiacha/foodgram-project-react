from django_filters import rest_framework as drf_filters
from django.contrib.auth import get_user_model

from recipes.models import Favorite, ShoppingCart, Recipe


User = get_user_model()


class RecipeFilter(drf_filters.FilterSet):
    is_favorited = drf_filters.BooleanFilter(field_name='in_favorited', method='filter_is_favorited')
    author = drf_filters.ModelChoiceFilter(field_name='author', queryset=User.objects.all())
    tags = drf_filters.CharFilter(field_name='tags__slug', lookup_expr='exact')
    
    def filter_is_favorited(self, queryset, name, value):
        # TODO: написать фильтр, возвращающий при запросе is_favorited=1 (value=1) список избранных пользователем self.request.user
        if value == 1:
            return queryset.filter(in_favorited__user=self.request.user)
        return queryset
    
    def filter_is_in_shopping_cart(self, queryset, name, value):
        # TODO: написать то же, что и для is_favorited
        if value == 1:
            return queryset.filter(in_shopping_cart__user=self.request.user)
        return queryset
    
    class Meta:
        model = Recipe
        fields = ['in_favorited', 'in_shopping_cart', 'author', 'tags']