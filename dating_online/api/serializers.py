from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import SEX, User


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
