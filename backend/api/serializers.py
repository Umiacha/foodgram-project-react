import base64
from time import time
from pprint import pprint  # Для дебага. Удалить как закончу

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework.serializers import ModelSerializer, ImageField, SerializerMethodField, PrimaryKeyRelatedField, SlugRelatedField, IntegerField, CurrentUserDefault

from recipes.models import Ingredient, Tag, Recipe, RecipeIngredient, Favorite, ShoppingCart
from users.serializers import UserSerializer


User = get_user_model()


class Base64toImage(ImageField):
    """Custom field for receiving base64 string and sending image's URI."""
    # def to_representation(self, value):
    #     return value
    
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=str(int(time())) + f'.{ext}')
        return super().to_internal_value(data)


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit',]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class RecipeIngredientSerializer(ModelSerializer):
    """Сериализатор для создания связи между рецептом и количеством ингредиента."""
    id = PrimaryKeyRelatedField(source='ingredient', queryset=Ingredient.objects.all())
    name = SlugRelatedField(source='ingredient', slug_field='name', read_only=True)
    measurement_unit = SlugRelatedField(source='ingredient', slug_field='measurement_unit', read_only=True)
    amount = IntegerField(min_value=1)  # , read_only=True)
    
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipeSerializer(ModelSerializer):
    """Сериализатор для добавления, обновления и возвращения рецепта.
    Параллельно он некоторыми полями связан с сериализаторами тегов и ингредиентов."""
    ingredients = RecipeIngredientSerializer(many=True)
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64toImage()
    author = UserSerializer(read_only=True, default=CurrentUserDefault())
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time']
    
    def validate_author(self, value):
        # value = self.context.get('request').user  # Правильный способ, однако пока что костыль!
        value = 1
        return UserSerializer(User.objects.get(pk=value))
    
    # def validate_tags(self, value):
    #     validated_values = []
    #     for val in value:
    #         tag = Tag.objects.get(pk=val)
    #         validated_values.append(TagSerializer(tag).to_representation())
    #     return validated_values
    
    def create(self, validated_data):
        pprint(validated_data)
        # print(validated_data.get('ingredients').get('ingredient'))
        # pprint(self.initial_data)
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        # recipe_data = validated_data.copy()
        # recipe_data.pop('ingredients')
        # recipe = Recipe.objects.create(**recipe_data, author=User.objects.get(pk=1))
        recipe = Recipe.objects.create(**validated_data, author=User.objects.get(pk=1))
        # pprint(validated_data)
        for ingredient_data in ingredients_data:
            # print(ingredient_data.get('ingredient'))
            ingredient = ingredient_data.get('ingredient')
            amount = ingredient_data['amount']
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=amount)
        for tag in tags:
            recipe.tags.add(tag)
        return recipe
    
    def to_representation(self, instance):
        """Изменяется формат полей 'ingredients' и 'tags' в ответе.
        
        Порядок выдачи не соответствует API."""
        self.fields.pop('ingredients')
        self.fields.pop('tags')
        representation = super().to_representation(instance)
        representation['ingredients'] = RecipeIngredientSerializer(
            RecipeIngredient.objects.filter(recipe=instance).all(), many=True
        ).data
        representation['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return representation
    
    def get_is_favorited(self, obj):
        user = self.context.get('request', None).user
        if not user.is_authenticated:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()
    
    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request', None).user
        if not user.is_authenticated:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()