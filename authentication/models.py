import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import mobile_validators


class UserManager(BaseUserManager):
    def create_user(self, mobile, email, first_name, last_name, password=None):
        """
        Create and return a `User` with an mobile, email, name and password.
        """
        user = self.model(
            mobile=mobile,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_mobile_verified=False,
            is_active=False,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, email, first_name, last_name, password=None):
        """
        Create and return a `User` wit2h superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(mobile, email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_mobile_verified = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        indexes = [
            models.Index(fields=['mobile']),
            models.Index(fields=['email']),
        ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=128)
    mobile = models.CharField(unique=True, max_length=12, blank=True, null=True,
                              validators=mobile_validators,
                              help_text=_('Required. 12 digits including country code'),
                              error_messages={'unique': _("A user with that mobile number already exists."), })

    is_mobile_verified = models.BooleanField(null=False, default=False)
    is_active = models.BooleanField(null=False, default=False)
    is_staff = models.BooleanField(null=False, default=False)
    is_superuser = models.BooleanField(null=False, default=False)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['password']
