import django
from django.utils.encoding import smart_str
from django.utils.translation import gettext

django.utils.encoding.smart_text = smart_str
django.utils.translation.ugettext = gettext
from rest_framework_jwt.authentication import JSONWebTokenAuthentication  # noqa


class CustomJSONWebTokenAuthentication(JSONWebTokenAuthentication):
    def authenticate(self, request):
        tuple_response = super(CustomJSONWebTokenAuthentication, self).authenticate(request)
        return tuple_response

    def authenticate_credentials(self, payload):
        user = super(CustomJSONWebTokenAuthentication, self).authenticate_credentials(payload)
        # if user.jwt_issue_dt.timetuple() > payload['iat']:
        #     raise AuthenticationFailed('Invalid payload')
        # inja mishe bishtar hasas bood rooye parameter haye dakhele payload dar jwt
        return user
