from rest_framework.serializers import ModelSerializer, Field

from recipes.models import Ingredient, Tag, Recipe, RecipeIngredient


class Base64toImage(Field):
    """Custom field for receiving base64 string and sending image's URI."""
    def to_representation(self, value):
        return value


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit',]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class RecipeSerializer(ModelSerializer):
    """Сериализатор для добавления, обновления и возвращения рецепта.
    Параллельно он некоторыми полями связан с сериализаторами тегов и ингредиентов."""
    ...
    
    def to_internal_value(self, data):
        # TODO: переопределить метод для декодирования base64 при сохранении.
        # TODO: определить url и директории для сохранения картинок (пока что они сохраняются в корневую директорию проекта).
        return super().to_internal_value(data)


class RecipeIngredientSerializer(ModelSerializer):
    """Сериализатор для создания связи между рецептом и количеством ингредиента."""
    ...