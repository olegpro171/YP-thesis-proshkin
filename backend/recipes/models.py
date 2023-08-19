from django.db import models

import backend.constant_values as constant_values
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=constant_values.TAG_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Имя тега'
    )

    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет'
    )

    slug = models.SlugField(
        max_length=constant_values.TAG_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=constant_values.INGREDIENT_NAME_MAX_LENGTH,
        verbose_name='Название',
    )

    measurement_unit = models.CharField(
        max_length=constant_values.INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH,
        verbose_name='Еденица измерения',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return f'{self.name[:10]}, {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(
        max_length=constant_values.RECIPE_NAME_MAX_LENGTH,
        verbose_name='Название',
    )

    text = models.TextField(
        verbose_name='Описание'
    )

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
    )

    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/image/',
        blank=True,
        null=True,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )

    tags = models.ManyToManyField(
        Tag,
        through='TagToRecipe',
        verbose_name='Теги',
        related_name='recipes'
    )

    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientInRecipe',
        verbose_name='Ингридиенты',
        related_name='recipes'
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = ('Рецепт')
        verbose_name_plural = ('Рецепты')
        constraints = [
            models.UniqueConstraint(
                fields=['text', 'author'],
                name='unique_text_author'
            )
        ]

    def __str__(self):
        return self.name[:10]


class TagToRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Теги в рецептах'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'],
                name='unique_tag_recipe'
            )
        ]


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='IngredientsToRecipes',
        verbose_name='Ингридиент',
    )

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='рецепт',
        related_name='IngredientsToRecipes'
    )

    amount = models.IntegerField(
        verbose_name='Количество',
        default=1
    )

    class Meta:
        verbose_name = 'Ингридиенты в рецептах'
        verbose_name_plural = verbose_name


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        related_name="in_favorites",
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="favorites",
        on_delete=models.CASCADE,
    )

    date_added = models.DateTimeField(
        verbose_name="Дата добавления",
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "recipe",
                    "user",
                ),
                name="unique_favorite_recipe_user",
            ),
        )

    def __str__(self) -> str:
        return f"{self.user} -> {self.recipe}"


class Cart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        related_name="in_cart",
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="cart",
        on_delete=models.CASCADE,
    )

    date_added = models.DateTimeField(
        verbose_name="Дата добавления",
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = "Рецепт в списке покупок"
        verbose_name_plural = "Рецепты в списке покупок"
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "recipe",
                    "user",
                ),
                name='unique_cart_recipe_user',
            ),
        )

    def __str__(self) -> str:
        return f"{self.user} -> {self.recipe}"
