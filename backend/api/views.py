from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient, Tag, Recipe

from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer
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
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = RecipeFilter
    
    def perform_create(self, serializer):
        # serializer.save(author=self.request.user)  # Решил перенести в валидацию поля в сериализаторе (его зона ответственности). Поменять, если не подойдет!
        serializer.save()