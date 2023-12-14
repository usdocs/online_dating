from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.include.filters import DistanceFilter
from api.serializers import (CoordinatesSerializer, CreateClientSerializer,
                             MatchClientSerializer, RetrieveClientSerializer,
                             TokenSerializer)
from users.models import User


class CreateClientViewSet(mixins.CreateModelMixin,
                          GenericViewSet):
    """Регистрация пользователя"""
    serializer_class = CreateClientSerializer

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(IsAuthenticated,),
        serializer_class=CoordinatesSerializer
    )
    def coordinates(self, request):
        """Фиксирует текущие координаты"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthClientViewSet(GenericViewSet):
    """Авторизация и разлогинивание"""
    serializer_class = TokenSerializer

    @action(
        detail=False,
        methods=['post'],
    )
    def login(self, request):
        """Выдает токен авторизации по емейлу и паролю"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.instance['response'],
            status=serializer.instance['status']
        )

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(IsAuthenticated,),
    )
    def logout(self, request):
        """Удаляет токен авторизации"""
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveMatchClientViewSet(mixins.RetrieveModelMixin,
                                 GenericViewSet):
    """Получение данных пользователя"""
    queryset = User.objects.all()
    serializer_class = MatchClientSerializer

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,),
    )
    def match(self, request, pk):
        """Эндпоинт оценивания участником, только для авторизованных!"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.instance, status=status.HTTP_201_CREATED)


class ListClientViewSet(mixins.ListModelMixin,
                        GenericViewSet):
    """Получение списка пользователей с фильтрацией"""
    serializer_class = RetrieveClientSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('sex', 'first_name', 'last_name')
    filterset_class = DistanceFilter

    def get_queryset(self):
        return User.objects.select_related('coordinates').exclude(
            id=self.request.user.id
        )
