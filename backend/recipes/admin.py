from django.contrib import admin
from django.contrib.admin import register

from django.contrib.admin import (
    ModelAdmin,
    TabularInline,
    display,
    register,
    site,
)

from . import models


@register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'color')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@register(models.TagToRecipe)
class TagToRecipeAdmin(admin.ModelAdmin):
    list_display = ('tag', 'recipe')
    list_filter = ('tag', 'recipe')
    search_fields = ('tag', 'recipe')


@register(models.IngredientToRecipe)
class IngredientToRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    list_filter = ('ingredient', 'recipe')
    search_fields = ('ingredient', 'recipe')
    list_per_page = 20


@register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time', 'author', 'pub_date')
    list_filter = ('author', 'tags', 'ingredients')
    search_fields = ('name', 'author')
    date_hierarchy = 'pub_date'
    filter_horizontal = ('tags', 'ingredients')


@register(models.Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ("user", "recipe", "date_added")
    search_fields = ("user__username", "recipe__name")


@register(models.Cart)
class CardAdmin(ModelAdmin):
    list_display = ("user", "recipe", "date_added")
    search_fields = ("user__username", "recipe__name")
