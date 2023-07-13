from django_filters import rest_framework
from geopy.distance import great_circle


class DistanceFilter(rest_framework.FilterSet):
    distance = rest_framework.NumberFilter(
        method='get_distance',
        label='distance',
    )

    def get_distance(self, queryset, name, value):
        """Фильтр на основе вычисления расстояния"""
        user_list = queryset.exclude(coordinates=None)
        self_location = (
                self.request.user.coordinates.latitude,
                self.request.user.coordinates.longitude
            )
        user_list_distance = user_list
        for user in user_list:
            location_client = (
                user.coordinates.latitude,
                user.coordinates.longitude
            )
            distance = great_circle(location_client, self_location).km
            if distance > float(value):
                user_list_distance = user_list_distance.exclude(id=user.id)
        return user_list_distance
