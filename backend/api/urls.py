from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteView,
                    IngredientView,
                    RecipeView,
                    ShoppingCartViewSet,
                    TagView,
                    shopping_cart_view)
from users.views import CustomUserViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagView, basename='tags')
router_v1.register('ingredients', IngredientView, basename='ingredients')
router_v1.register('recipes', RecipeView, basename='recipes')
router_v1.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),

    path("recipes/download_shopping_cart/",
         shopping_cart_view,
         name="download"),

    path("recipes/<int:recipe_id>/shopping_cart/",
         ShoppingCartViewSet.as_view()),

    path("recipes/<int:recipe_id>/favorite/", FavoriteView.as_view()),

    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
]
