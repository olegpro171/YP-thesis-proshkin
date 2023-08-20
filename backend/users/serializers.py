import djoser.serializers
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

from .models import User, Follow
from recipes.models import Recipe


class SpecialRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class CustomUserSerializer(djoser.serializers.UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'id',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
            )
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if self.context.get('request').user.is_anonymous:
            return False
        return obj.following.filter(subcribed_to=request.user).exists()


class UserCreateSerializer(djoser.serializers.UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        validators = (

        )


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    subscriber = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    subcribed_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    def validate(self, data):
        subscriber = data.get('subscriber')
        subcribed_to = data.get('subcribed_to')
        if subscriber == subcribed_to:
            raise serializers.ValidationError('Self-following is not allowed')

        if Follow.objects.filter(
            subscriber=subscriber,
            subcribed_to=subcribed_to
        ).exists():
            raise serializers.ValidationError('Subscription already exists')

        return data

    class Meta:
        model = Follow
        fields = ('subscriber', 'subcribed_to')
        validators = []


class FollowerSerializer(serializers.ModelSerializer):
    recipes = SpecialRecipeSerializer(many=True, required=True)
    is_subscribed = serializers.SerializerMethodField('check_is_subscrobed')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]

    def get_recipes_count(self, obj):
        count = obj.recipes.all().count()
        return count

    def check_is_subscrobed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return obj.following.filter(subcribed_to=request.user).exists()
