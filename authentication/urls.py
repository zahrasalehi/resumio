from django.urls import path
from .views import *

app_name = 'authentication'
urlpatterns = [
    path(r'otp/', OneTimePasswordView.as_view()),

    # dovomin api ke call mishe va profile ro update mikone
    # mishe ke model profile kollan joda bashe az UserModel va ba'd az register profile ro update konim
    # amma felan baraye rahati kar simple fekr mikonim :)
    path(r'profile/update', UpdateProfileView.as_view()),

    path(r'obtain/', CustomObtainJSONWebToken.as_view()),
    path(r'refresh/', CustomRefreshJSONWebToken.as_view()),

    path(r'me/', ProfileView.as_view()),
]
