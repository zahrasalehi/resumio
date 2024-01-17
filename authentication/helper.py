from datetime import timedelta
from random import randint

import pytz
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError, PermissionDenied

from resumio.resumio import settings


def redis_key_eligible(key, ex, max_attempt=settings.MAX_CODE_ATTEMPT):
    attempt = 0
    key_count = f'{key}_count'
    try:
        if settings.redis_client.exists(key_count):
            attempt = settings.redis_client.get(key_count)
    except Exception:
        pass
    settings.redis_client.set(
        key_count,
        int(attempt) + 1,
        ex=ex,
    )
    return int(attempt) < int(max_attempt)  # TODO: * 2


def mobile_code(prefix, mobile, write=True):
    key = f'{prefix}_{mobile}'
    otp_code_expire_time = int(settings.OTP_CODE_EXPIRE_TIME.total_seconds())
    block_time = int(settings.OTP_BLOCK_TIME.total_seconds())

    if redis_key_eligible(key, ex=block_time):
        if settings.redis_client.exists(key):
            code = settings.redis_client.get(key)
            return int(code)
        elif write:
            code = str(randint(100000, 999999))
            settings.redis_client.set(
                key,
                code,
                ex=otp_code_expire_time,
            )
            return int(code)
    elif write:
        raise PermissionDenied(detail=_('You submitted reset code more than expected. Please try again later'))
    else:
        # preventing time based attack
        return randint(999999, 9999999)

