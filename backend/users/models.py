from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField


# Мб добавить роли как поле?
class CustomUser(AbstractUser):
    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150)
    email = EmailField(max_length=254)
    
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f'Пользователь {self.username}'
