from django.urls import reverse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APITransactionTestCase
# from rest_framework.authtoken.models import Token

from recipes.models import Ingredient, Tag
from users.models import CustomUser


class IngredientApiTestCase(APITransactionTestCase):
    """Tests for Ingredient's API."""
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.url = reverse('ingredients-list')
    
    def setUp(self) -> None:
        self.user: CustomUser = CustomUser.objects.create(username='customer')
        self.ingr_1 = Ingredient.objects.create(name='Salt', measurement_unit='kg')
        self.ingr_2 = Ingredient.objects.create(name='Water', measurement_unit='ml')
        self.ingr_url = self.url + f'{self.ingr_1.id}/'
    
    def test_get_list_ingredients(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'Убедитесь, что {self.url} доступна для пользователей!')
        answer = [model_to_dict(ingr) for ingr in Ingredient.objects.all()]
        self.assertEqual(response.data, answer, f'Убедитесь, что при запросе {self.url} возвращается полный список ингредиентов!')
    
    def test_retrieve_ingredient(self):
        # ingr_url = self.url + f'{self.ingr_1.id}/'
        response = self.client.get(self.ingr_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'Убедитесь, что страница {self.ingr_url} доступна!')
        self.assertEqual(response.data, model_to_dict(self.ingr_1), f'Убедитесь, что при запросе по {self.ingr_url} возвращается ингредиент с id={self.ingr_1.id}!')
    
    def test_startswith_filter_search_on_name(self):
        correct_filter_url = {'search': self.ingr_1.name[0]}
        incorrect_filter_url = {'search': self.ingr_1.name[1]}
        correct_response = self.client.get(self.url, correct_filter_url)
        incorrect_response = self.client.get(self.url, incorrect_filter_url)
        self.assertEqual(correct_response.status_code, status.HTTP_200_OK, 'Убедитесь, что запрос с поиском по первой букве возвращает ингредиент!')
        self.assertEqual(incorrect_response.status_code, status.HTTP_200_OK, 'Убедитесь, что запрос и по неподходящему фильтру доступен!')
        self.assertEqual(correct_response.data, [model_to_dict(self.ingr_1)], 'Убедитесь, что на запрос по фильтру возвращается список подходящих ингредиентов!')
        self.assertEqual(incorrect_response.data, [], 'Убедитесь, что при отсутствии совпадений по фильтру возвращается пустой список.')


class TagApiTestCase(APITransactionTestCase):
    """Tests for Tag's API."""
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.url = reverse('tags-list')
    
    def setUp(self) -> None:
        self.user: CustomUser = CustomUser.objects.create(username='customer')
        self.tag_1 = Tag.objects.create(name='Sweet', color='#49B64E', slug='sweet')
        self.tag_2 = Tag.objects.create(name='Spicy', color='#FF0000', slug='spicy')
        self.tag_url = self.url + f'{self.tag_1.id}/'
    
    def test_get_list_tags(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'Убедитесь, что {self.url} доступна для пользователей!')
        answer = [model_to_dict(tag) for tag in Tag.objects.all()]
        self.assertEqual(response.data, answer, f'Убедитесь, что при запросе {self.url} возвращается полный список тегов!')
    
    def test_retrieve_tag(self):
        # ingr_url = self.url + f'{self.ingr_1.id}/'
        response = self.client.get(self.tag_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'Убедитесь, что страница {self.tag_url} доступна!')
        self.assertEqual(response.data, model_to_dict(self.tag_1), f'Убедитесь, что при запросе по {self.tag_url} возвращается ингредиент с id={self.tag_1.id}!')
