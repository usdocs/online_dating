from django.contrib.auth.hashers import make_password
from geopy.distance import great_circle
from rest_framework import serializers
from users.models import SEX, Coordinates, User


class CreateClientSerializer(serializers.ModelSerializer):
    sex = serializers.ChoiceField(choices=SEX)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('profile_picture', 'sex', 'first_name', 'last_name', 'email',
                  'username', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(CreateClientSerializer, self).create(validated_data)


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class RetrieveClientSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('profile_picture', 'sex', 'first_name', 'last_name', 'email',
                  'username', 'distance')

    def get_distance(self, obj):
        request = self.context.get('request')
        if (Coordinates.objects.filter(user=obj) and
           Coordinates.objects.filter(user=request.user)):
            location_client = (
                obj.coordinates.latitude,
                obj.coordinates.longitude
            )
            self_location = (
                request.user.coordinates.latitude,
                request.user.coordinates.longitude
            )
            return great_circle(location_client, self_location).km
        return ''


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ('longitude', 'latitude')
