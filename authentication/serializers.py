from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import JSONWebTokenSerializer, RefreshJSONWebTokenSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from .models import *
from .utils import *


class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):
    def __init__(self, *args, **kwargs):
        super(CustomJSONWebTokenSerializer, self).__init__(*args, **kwargs)

    @staticmethod
    def get_jwt_for_user(user, request):
        if user:
            payload: dict = jwt_payload_handler(user)
            refresh_payload: dict = jwt_refresh_payload_handler(user)
            return {
                'access_token': jwt_encode_handler(payload),
                'refresh_token': jwt_encode_handler(refresh_payload),
            }
        else:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg)

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)
            return CustomJSONWebTokenSerializer.get_jwt_for_user(user, self.context['request'])
        else:
            msg = _(f'Must include {self.username_field} and "password".')
            raise serializers.ValidationError(msg)


class CustomRefreshJSONWebTokenSerializer(RefreshJSONWebTokenSerializer):
    """
    Refresh an access token.
    """

    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        new_payload = jwt_payload_handler(user)
        refresh_payload = jwt_refresh_payload_handler(user)
        return {
            'access_token': jwt_encode_handler(new_payload),
            'refresh_token': jwt_encode_handler(refresh_payload),
            'id': user.id,
        }


class OneTimePasswordSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    mobile = serializers.CharField(validators=mobile_validators)
    code = serializers.IntegerField(min_value=000000, max_value=999999, required=False)
    password = serializers.CharField(max_length=255, required=False)
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
