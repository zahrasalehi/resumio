from rest_framework import status
from rest_framework.generics import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response as RestResponse
from rest_framework.status import HTTP_200_OK
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken

from .helper import mobile_code
from .serializers import *

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class UpdateProfileView(UpdateAPIView):
    http_method_names = ['patch']


class CustomObtainJSONWebToken(ObtainJSONWebToken):
    serializer_class = CustomJSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        Create JWT pair from given input

        Concrete view for creating a model instance.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            pair_token = serializer.object
            response = RestResponse(pair_token, status=HTTP_200_OK)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    pair_token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return RestResponse(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class CustomRefreshJSONWebToken(RefreshJSONWebToken):
    serializer_class = CustomRefreshJSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        Create JWT pair

        Create JWT pair from given input
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            token = serializer.object
            response = RestResponse(token)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return RestResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OneTimePasswordView(GenericAPIView):
    serializer_class = OneTimePasswordSerializer
    permission_classes = [AllowAny]

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """
        Send OneTimePassword SMS to mobile number

        Send SMS to mobile number from the given input
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            mobile = request.data.get('mobile')
            code = request.data.get('code', '')
            first_name = request.data.get('first_name', '')
            last_name = request.data.get('last_name', '')
            password = request.data.get('password', '')
            if code in (0, ''):
                code = mobile_code('otp', mobile)
                # send_sms.delay(receptor=mobile, token=code)
                # TODO: ye sms sender lazem hast baraye inke vaghean sms befrestim,
                # hamchenin baraye inke request kond nashe age sms sender latency dasht, sms ro tooye queue mindazim :)
                return RestResponse(status=status.HTTP_200_OK)
            elif int(code) == mobile_code('otp', mobile):
                try:
                    user = User.objects.get(mobile=mobile)
                    user.is_active = True
                    user.is_mobile_verified = True
                except User.DoesNotExist:
                    user = User(
                        mobile=mobile,
                        is_active=True,
                        is_mobile_verified=True,
                        first_name=first_name,
                        last_name=last_name,
                        password=make_password(password),
                    )
                user.save()
                jwt = CustomJSONWebTokenSerializer.get_jwt_for_user(user, request)
                return RestResponse(data=jwt, status=status.HTTP_200_OK)

        return RestResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return RestResponse(
            data=ProfileSerializer(instance=request.user).data
        )
