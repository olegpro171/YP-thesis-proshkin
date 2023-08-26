import io

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .filter import RecipeFilter
from .pagination import CustomPagination
from recipes.models import (Tag,
                            Recipe,
                            Ingredient,
                            IngredientInRecipe,
                            Favorite,
                            Cart,)


class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permissions = [AllowAny, ]
    pagination_class = None


class IngredientView(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = serializers.IngredientSerializer
    search_fields = ['name', ]
    pagination_class = None


class RecipeView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permissions = [IsAuthenticatedOrReadOnly, ]
    filter_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        method = self.request.method
        if method == 'POST' or method == 'PATCH':
            return serializers.CreateRecipeSerializer
        return serializers.GetRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        tags_slugs = self.request.query_params.getlist('tags')
        author = self.request.query_params.get('author')

        if is_favorited == '1' and self.request.user.is_authenticated:
            queryset = queryset.filter(
                in_favorites__user=self.request.user
            ).distinct()

        if is_in_shopping_cart == '1' and self.request.user.is_authenticated:
            queryset = queryset.filter(
                in_cart__user=self.request.user
            ).distinct()

        if tags_slugs:
            queryset = queryset.filter(tags__slug__in=tags_slugs).distinct()

        if author == 'me':
            author = self.request.user.id
        elif author is str:
            author = int(author)

        if author:
            queryset = queryset.filter(author__id=author).distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FavoriteView(APIView):
    permissions = [IsAuthenticatedOrReadOnly, ]

    @action(methods=['post'], detail=True)
    def post(self, request, recipe_id):
        user = request.user
        data = {
            'user': user.id,
            'recipe': recipe_id,
        }
        serializer = serializers.FavoriteSerializer(
            data=data, context={'request': request, 'recipe_id': recipe_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['DELETE'], detail=True)
    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if not user.favorites.filter(recipe=recipe).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Favorite.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = None

    @action(methods=['post'], detail=True)
    def post(self, request, recipe_id):
        user = request.user
        data = {'user': user.id, 'recipe': recipe_id}
        serializer = serializers.ShoppingCartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(method=('delete',), detail=True)
    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if not user.cart.filter(recipe=recipe).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Cart.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def shopping_cart_view(request):
    user = request.user
    all_carts = user.cart.all()

    ingredients_list = {}

    for cart_item in all_carts:
        ingredients = IngredientInRecipe.objects.filter(
            recipe=cart_item.recipe
        )

        for ingredient in ingredients:
            key = ingredient.ingredient.name
            amount = ingredient.amount
            measurement_unit = ingredient.ingredient.measurement_unit

            try:
                ingredients_list[key]['amount'] += amount
            except KeyError:
                ingredients_list[key] = {
                    'M_U': measurement_unit,
                    'amt': amount,
                }

    file_strings = []

    for key, data in ingredients_list.items():
        file_strings.append(f"{key} - {data['amt']} {data['M_U']}")

    file_content = '\n'.join(file_strings).encode('utf-8')
    file_name = 'shopping_cart.txt'
    text_file = io.BytesIO(file_content)
    text_file.seek(0)

    response = FileResponse(text_file, content_type='text/plain')
    response['Content-Disposition'] = f"attachment; filename='{file_name}'"
    return response
