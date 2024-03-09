from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter

from .views import IngredientViewSet, TagViewSet


router = SimpleRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
]