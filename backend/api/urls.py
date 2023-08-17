from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsView, RecipeView, TagView
from users.views import CustomUserViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagView, basename='tags')
router_v1.register('ingredients', IngredientsView, basename='ingredients')
router_v1.register('recipes', RecipeView, basename='recipes')
router_v1.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
