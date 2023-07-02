from math import cos, radians

from django_filters import rest_framework
from geopy.distance import great_circle
from users.models import User


class DistanceFilter(rest_framework.FilterSet):
    distance = rest_framework.NumberFilter(
        method='get_distance',
        label='distance',
    )
    distance2 = rest_framework.NumberFilter(
        method='get_distance_2',
        label='distance',
    )

    def get_distance(self, queryset, name, value):
        """Фильтр на основе фильтрации по координатам. Не очень точный"""
        mylon = self.request.user.coordinates.longitude
        mylat = self.request.user.coordinates.latitude
        lat1 = mylat - (float(value) / 111.0)
        lat2 = mylat + (float(value) / 111.0)
        lon1 = mylon - float(value) / abs(cos(radians(mylat)) * 111.0)
        lon2 = mylon + float(value) / abs(cos(radians(mylat)) * 111.0)
        user_list = User.objects.filter(
            coordinates__latitude__gte=lat1, coordinates__latitude__lte=lat2
        ).filter(
            coordinates__longitude__gte=lon1, coordinates__longitude__lte=lon2
        )
        return user_list.exclude(id=self.request.user.id)

    def get_distance_2(self, queryset, name, value):
        """Фильтр на основе вычисления расстояния, нагружает БД"""
        user_list = queryset.exclude(id=self.request.user.id)
        user_list_distance = user_list
        distance_param = self.request.GET.get('distance2')
        if distance_param:
            self_location = (
                    self.request.user.coordinates.latitude,
                    self.request.user.coordinates.longitude
                )
            for user in user_list:
                location_client = (
                    user.coordinates.latitude,
                    user.coordinates.longitude
                )
                distance = great_circle(location_client, self_location).km
                if distance > float(distance_param):
                    user_list_distance = user_list.exclude(id=user.id)
        return user_list_distance
