from api.serializers import CreateClientSerializer, TokenSerializer
from django.contrib.auth.hashers import check_password
from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from users.models import User


class CreateClientViewSet(mixins.CreateModelMixin,
                          GenericViewSet):
    """Регистрация пользователя"""
    serializer_class = CreateClientSerializer


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
