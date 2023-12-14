from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from geopy.distance import great_circle
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token

from api.include.send_mail import send_mail_match
from api.include.watermark import watermark_with_transparency
from users.models import SEX, Coordinates, Match, User


class CreateClientSerializer(serializers.ModelSerializer):
    sex = serializers.ChoiceField(choices=SEX)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('profile_picture', 'sex', 'first_name', 'last_name', 'email',
                  'username', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['profile_picture'] = watermark_with_transparency(
            validated_data['profile_picture'],
            settings.WATERMARK_URL,
            position=settings.WATERMARK_POSITION
        )
        return super(CreateClientSerializer, self).create(validated_data)


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password')
        read_only_fields = ('email', 'password')

    def to_internal_value(self, data):
        return data

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if not user:
            raise serializers.ValidationError(
                'Пользователя с таким email не существует'
            )
        if not check_password(attrs['password'], user.password):
            raise serializers.ValidationError(
                'Введен неверный пароль'
            )
        return attrs

    def create(self, validated_data):
        token, created = Token.objects.get_or_create(
            user=User.objects.filter(email=validated_data['email']).first()
        )
        if created:
            stat = status.HTTP_201_CREATED
        else:
            stat = status.HTTP_200_OK
        return {'response': {'auth_token': str(token)}, 'status': stat}


class RetrieveClientSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('profile_picture', 'sex', 'first_name', 'last_name',
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

    def create(self, validated_data):
        coordinates = Coordinates.objects.filter(
            user=self.context.get('request').user
        ).first()
        if coordinates:
            coordinates.delete()
        return super(CoordinatesSerializer, self).create(validated_data)


class MatchClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_picture', 'sex', 'first_name', 'last_name',
                  'username')
        read_only_fields = ('profile_picture', 'sex', 'first_name',
                            'last_name', 'username')

    def validate(self, attrs):
        if self.context['request'].user == self.instance:
            raise serializers.ValidationError(
                'Вы не можете проявить симпатию к себе)'
            )
        return attrs

    def update(self, instance, validated_data):
        user = self.context['request'].user
        match, created = Match.objects.get_or_create(
            user=user,
            liking=instance
        )
        if created:
            raise serializers.ValidationError(
                'Вы уже проявили симпатию к данному пользователю'
            )
        if instance.liker.filter(liking=user).first():
            send_mail_match(user, instance)
            send_mail_match(instance, user)
            return {'email': instance.email}
        return MatchClientSerializer(instance).data
