from typing import Dict, Union

from django.db.utils import DatabaseError
from django.db.models.query import QuerySet
from django.test import TestCase

from .models import CustomUser

# 1) Написать тесты для проверки CRUD модели пользователей.  <- Избыточно. Не пишем!
# 2) Написать тесты для проверки эндпоинтов api/users/.
# 3) Проверить регистрацию, аутентификацию и смену пароля пользователем (??).


# class TestUsersCRUD(TestCase):
#     USER_DATA: Dict[str, Union[str, int]] = {
#         'email': 'sample@sample.com',
#         'username': 'SimpleSample',
#         'first_name': 'Sam',
#         'last_name': '1234',
#         'password': 'somepassword',
#     }
#     # @classmethod
#     # def setUpTestData(cls) -> None:
#     #     ...
    
#     def test_user_create(self):
#         before_creation: int = len(CustomUser.objects.all())  # Наверное тут надо как-то заставить запрос прокинуться СРАЗУ!
#         try:
#             new_user: CustomUser = CustomUser.objects.create(  # Либо вынести в отдельную функцию (не раз делаю), либо в classmethod.
#                 **self.USER_DATA
#             )
#         except DatabaseError:
#             raise Exception('Возникла проблема с БД '
#                             'при попытке создать пользователя!')
#         after_creation: int = len(CustomUser.objects.all())
#         self.assertEqual(
#             after_creation - before_creation, 1,
#             'Убедитесь, что при корректном запросе к БД пользователь создается!'
#         )
    
#     def test_user_get(self):
#         ...
    
#     def test_user_update(self):
#         ...
    
#     def test_user_deleting(self):
#         new_user: CustomUser = CustomUser.objects.create(
#             **self.USER_DATA
#         )
#         try:
#             new_user.delete()
#         except DatabaseError:
#             raise Exception('Запрос на удаление пользователя к БД не прошел!')


class TestUsersApi(TestCase):
    ...


class TestUsersAuth(TestCase):
    ...
