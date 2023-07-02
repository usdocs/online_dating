from api.include.filters import DistanceFilter
from api.include.send_mail import send_mail_match
from api.include.watermark import watermark_with_transparency
from api.serializers import (CoordinatesSerializer, CreateClientSerializer,
                             RetrieveClientSerializer, TokenSerializer)
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from users.models import Coordinates, Match, User


class CreateClientViewSet(mixins.CreateModelMixin,
                          GenericViewSet):
    """Регистрация пользователя"""
    serializer_class = CreateClientSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile_picture_with_watermark = watermark_with_transparency(
            request.data['profile_picture'],
            settings.WATERMARK_URL,
            position=settings.WATERMARK_POSITION
        )
        serializer.save(profile_picture=profile_picture_with_watermark)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(IsAuthenticated,),
        serializer_class=CoordinatesSerializer
    )
    def coordinates(self, request):
        """Фиксирует текущие координаты"""
        coordinates = Coordinates.objects.filter(user=request.user).first()
        if coordinates:
            coordinates.delete()
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
        user = User.objects.filter(email=request.data['email']).first()
        if not user:
            return Response(
                {'Пользователя с таким email не существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not check_password(request.data['password'], user.password):
            return Response(
                {'Введен неверный пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token, created = Token.objects.get_or_create(user=user)
        if created:
            stat = status.HTTP_201_CREATED
        else:
            stat = status.HTTP_200_OK
        response = {'auth_token': str(token)}
        return Response(response, status=stat)

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
    serializer_class = RetrieveClientSerializer

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,),
    )
    def match(self, request, pk):
        """Эндпоинт оценивания участником, только для авторизованных!"""
        liking_user = get_object_or_404(User, id=pk)
        user = get_object_or_404(User, username=self.request.user.username)
        if str(user.id) == pk:
            return Response(
                {'Вы не можете проявить симпатию к себе)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        match, created = Match.objects.get_or_create(
            user=user,
            liking=liking_user
        )
        if not created:
            return Response(
                {'Вы уже проявили симпатию к данному пользователю'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(liking_user)
        if liking_user.liker.filter(liking=user).first():
            send_mail_match(user, liking_user)
            send_mail_match(liking_user, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListClientViewSet(mixins.ListModelMixin,
                        GenericViewSet):
    """Получение списка пользователей с фильтрацией"""
    queryset = User.objects.all()
    serializer_class = RetrieveClientSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('sex', 'first_name', 'last_name')
    filterset_class = DistanceFilter
