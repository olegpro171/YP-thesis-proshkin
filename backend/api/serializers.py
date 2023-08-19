from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

import recipes.models as models
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = '__all__'
        read_only_fields = ('id', 'name', 'measurement_unit',)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IngredientInRecipe
        fields = '__all__'
        read_only_fields = ('id', 'name', 'measurement_unit',)


class GetRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = serializers.SerializerMethodField('get_ingredients')
    is_favorited = serializers.SerializerMethodField('is_favorite')
    is_in_shopping_cart = serializers.SerializerMethodField(
        'check_is_in_shopping_cart'
    )
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = models.Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        ingredients = models.IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def check_is_favorite(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return models.Favorite.objects.filter(recipe=obj, user=user).exists()

    def check_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return models.Cart.objects.filter(
            recipe=obj, user=user
        ).exists()


class AddIngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=models.Ingredient.objects.all()
    )

    class Meta:
        model = models.IngredientInRecipe
        fields = ('id', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    cooking_time = serializers.IntegerField()
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = AddIngredientInRecipeSerializer(many=True)
    tags = serializers.SlugRelatedField(
        many=True, queryset=models.Tag.objects.all(), slug_field='id'
    )

    class Meta:
        model = models.Recipe
        fields = '__all__'

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError('Invalid cooking time')
        return data

    def validate(self, data):
        user = self.context.get('request').user
        text = data.get('text')

        # Exclude current instance if it exists (for update)
        if self.instance:
            existing_recipes = user.recipes.filter(
                text=text).exclude(pk=self.instance.pk)
        else:
            existing_recipes = user.recipes.filter(text=text)

        if existing_recipes.exists():
            raise serializers.ValidationError('Recipe already exists')

        return data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = models.Recipe.objects.create(author=author, **validated_data)

        for ingredient in ingredients_data:
            ingredient_model = ingredient.get('id')
            amount = ingredient.get('amount')
            models.IngredientInRecipe.objects.create(
                ingredient=ingredient_model, recipe=recipe, amount=amount
            )

        recipe.tags.set(tags_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.get('ingredients')
        tags_data = validated_data.get('tags')

        models.TagToRecipe.objects.filter(recipe=instance).delete()

        if not ingredients_data:
            raise serializers.ValidationError('No ingredients provided')
        models.IngredientInRecipe.objects.filter(recipe=instance).delete()

        for ingredient in ingredients_data:
            ingredient_model = ingredient['id']
            amount = ingredient['amount']
            models.IngredientInRecipe.objects.create(
                ingredient=ingredient_model, recipe=instance, amount=amount
            )
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.tags.set(tags_data)
        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=models.Recipe.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all()
    )

    class Meta:
        model = models.Favorite
        fields = ['recipe', 'user']

    def validate(self, attrs):
        user = self.context.get('request').user
        recipe_id = self.context.get('recipe_id')
        if models.Favorite.objects.filter(user=user,
                                          recipe__id=recipe_id).exists():
            raise serializers.ValidationError('Recipe already in favorites')

        return super().validate(attrs)


class ShoppingCartSerializer(FavoriteSerializer):
    class Meta:
        model = models.Cart
        fields = ['recipe', 'user']
        validators = [
            UniqueTogetherValidator(
                queryset=models.Cart.objects.all(),
                fields=['user', 'recipe'],
            )
        ]
