from djoser.views import UserViewSet
from rest_framework import viewsets

from .serializers import RecipeSerializer
from recipes.models import Tag, Ingredient, Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
