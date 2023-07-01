import base64

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from rest_framework import serializers
from users.models import SEX, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CreateClientSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField()
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
