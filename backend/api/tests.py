from django.urls import reverse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APITransactionTestCase
# from rest_framework.authtoken.models import Token

from recipes.models import Ingredient
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
    
    def test_get_list_ingredients(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'Убедитесь, что {self.url} доступна для пользователей!')
        answer = [model_to_dict(ingr) for ingr in Ingredient.objects.all()]
        self.assertEqual(response.data, answer, f'Убедитесь, что при запросе {self.url} возвращается полный список ингредиентов!')
    
    def test_retrieve_ingredient(self):
        ingr_url = self.url + f'{self.ingr_1.id}/'
        response = self.client.get(ingr_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'Убедитесь, что страница {ingr_url} доступна!')
        self.assertEqual(response.data, model_to_dict(self.ingr_1), f'Убедитесь, что при запросе по {ingr_url} возвращается ингредиент с id={self.ingr_1.id}!')