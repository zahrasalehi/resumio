from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthenticationConfig(AppConfig):
    name = 'authentication'
    label = 'authentication'
    verbose_name = _('Authentication App')
