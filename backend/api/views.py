from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action

from recipes.models import Ingredient, Tag, Recipe

from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer, FavoriteSerializer, ShoppingCartSerializer
# from .filters import RecipeFilter

from django.contrib.auth import get_user_model


User = get_user_model()


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^name']


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'put', 'delete', 'head']
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = RecipeFilter
    
    def update(self, request, *args, **kwargs):
        """Обновление рецепта путем удаления предыдущего и создания абсолютно такого же, но с изменениями пользователя."""
        Recipe.objects.get(pk=kwargs.get('pk')).delete()
        return self.create(request, *args, **kwargs)
    
    @action(
        detail=True,
        # permission_classes=[],  # Пермишены: только для авторизованного пользователя.
        methods=['post'],
        url_path='favorite',
        url_name='favorite'
    )
    def add_to_favorite(self, request):
        return self.add_to_list(request, model=Recipe, serializer_class=FavoriteSerializer)
    
    def add_to_list(self, request, model, serializer_class):  # TODO: добавить методы add_to_list и remove_from_list для Favorite и ShoppingCart (см. Пачку).
        """Создает объект сериализатора для сохранения записи в таблицу. Возвращает ошибки сериализатор или краткое содержание рецепта."""
        model = get_object_or_404(Recipe, pk=request.data.get('pk'))
        serializer = serializer_class(user=request.user, recipe=model)
        if serializer.is_valid():
            serializer.save()
        # model.objects.create(user=request.user, recipe=model)