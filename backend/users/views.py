from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    CustomUserSerializer,
    PasswordSerializer,
    ShowFollowerSerializer,
    FollowerSerializer,
)
from .models import Follow, User


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        AllowAny,
    ]
    pagination_class = None
 
    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = CustomUserSerializer(user, context={"request": request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"status": "password set"})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=["get", "delete", "post"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, pk=None):
        user = request.user
        sub_to = get_object_or_404(User, pk=pk)
        follow = Follow.objects.filter(subscriber=user, subcribed_to=sub_to)
        data = {
            'subscriber': user.id,
            'subcribed_to': sub_to.id,
        }
        if request.method == "GET" or request.method == "POST":
            serializer = FollowerSerializer(data=data, context=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=["get", "post"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        follow = Follow.objects.filter(subscriber=user)

        subscribed_to_users = follow.values_list('subcribed_to', flat=True)
        subscribed_users = User.objects.filter(pk__in=subscribed_to_users)

        paginator = PageNumberPagination()
        paginator.page_size = 6

        result_page = paginator.paginate_queryset(subscribed_users, request)
        serializer = ShowFollowerSerializer(
            result_page,
            many=True,
            context={"current_user": user}
        )
        
        return paginator.get_paginated_response(serializer.data)
