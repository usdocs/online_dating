from api.views import (AuthClientViewSet, CreateClientViewSet,
                       ListClientViewSet, RetrieveMatchClientViewSet)
from django.urls import include, path
from rest_framework import routers

v1_router = routers.DefaultRouter()
v1_1_router = routers.DefaultRouter()
v1_router.register('create',
                   CreateClientViewSet,
                   basename='user_create')
v1_router.register('auth',
                   AuthClientViewSet,
                   basename='user_auth')
v1_router.register('',
                   RetrieveMatchClientViewSet,
                   basename='user_retrive')
v1_1_router.register('',
                     ListClientViewSet,
                     basename='user_list')

urlpatterns = [
    path('clients/', include(v1_router.urls)),
    path('list/', include(v1_1_router.urls))
]
