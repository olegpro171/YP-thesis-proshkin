from django.contrib import admin
from django.contrib.admin import register

from . import models


@register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
    )
    search_fields = ('username',)
    list_filter = ('username', 'email')
    ordering = ('username',)
    empty_value_display = '-пусто-'


@register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'subscriber', 'subcribed_to'
    )
    search_fields = ('subscriber', 'subcribed_to')
    list_filter = ('subscriber', 'subcribed_to')
    ordering = ('subscriber',)
    empty_value_display = '-пусто-'
