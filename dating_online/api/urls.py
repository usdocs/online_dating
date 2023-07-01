from api.views import AuthClientViewSet, CreateClientViewSet
from django.urls import include, path
from rest_framework import routers

v1_router = routers.DefaultRouter()
v1_router.register('create',
                   CreateClientViewSet,
                   basename='user_create')
v1_router.register('auth',
                   AuthClientViewSet,
                   basename='user_auth')

urlpatterns = [
    path('clients/', include(v1_router.urls)),
]
