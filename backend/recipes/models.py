from django.db.models import Model, CharField, SlugField
from django.core.validators import RegexValidator


class Ingredient(Model):
    name = CharField(max_length=200, verbose_name='Название')
    measurement_unit = CharField(
        max_length=200, verbose_name='Единицы измерения'
    )
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(Model):
    name = CharField(
        max_length=200, verbose_name='Название', unique=True
    )
    color = CharField(
        max_length=7, verbose_name='Цвет', unique=True
    )
    slug = SlugField(
        max_length=200, verbose_name='Слаг', unique=True, validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )
    
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
    
    def __str__(self):
        return f'{self.name} {self.slug}'
