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

        def distance_calc(user):
            location_client = (
                user.coordinates.latitude,
                user.coordinates.longitude
            )
            if great_circle(location_client, self_location).km < float(value):
                return user.username
            return None

        list_distance = list(map(lambda user: distance_calc(user), user_list))
        return user_list.filter(username__in=list_distance)
