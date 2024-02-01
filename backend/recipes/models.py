from django.db.models import Model, CharField

# Create your models here. Создавай модели и отрабатывай по схеме из notes.txt
class Ingredients(Model):
    name = CharField(max_length=200, verbose_name='Название')
    measurement_unit = CharField(
        max_length=200, verbose_name='Единицы измерения'
    )
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return f'{self.name} {self.measurement_unit}'
