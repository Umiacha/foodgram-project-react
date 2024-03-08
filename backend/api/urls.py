from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import IngredientViewSet


router = SimpleRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]