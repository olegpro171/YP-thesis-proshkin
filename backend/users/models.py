from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q


import backend.constant_values as constant_values


class User(AbstractUser):
    first_name = models.CharField(
        max_length=constant_values.USER_FIRST_NAME_MAX_LENGTH,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=constant_values.USER_LAST_NAME_MAX_LENGTH,
        verbose_name='Фамилия'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    subscriber = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )

    subcribed_to = models.ForeignKey(
        User,
        related_name='followers',
        verbose_name='Подисан на',
        on_delete=models.CASCADE,
    )

    datetime = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Дата подписки',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "subscriber",
                    "subcribed_to",
                ),
                name="unique_follow",
            ),
            models.CheckConstraint(
                check=~Q(subscriber=F('subcribed_to')),
                name='no_self_follow'
            )
        )

    def __str__(self):
        return f'{self.subscriber} -> {self.subcribed_to}'
