from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, EmailField, ForeignKey, CASCADE, UniqueConstraint


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


class Following(Model):
    follower = ForeignKey(
        CustomUser, on_delete=CASCADE, related_name='following', verbose_name='Подписчик'
    )
    author = ForeignKey(
        CustomUser, on_delete=CASCADE, related_name='follower', verbose_name='Автор'
    )
    
    class Meta:
        constraints = [UniqueConstraint(
            fields=('follower', 'author'),
            name='unique_subscribe'
        ),]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
    
    def __str__(self):
        return f'{self.follower} подписан на {self.author}'
