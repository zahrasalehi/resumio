from django.core.validators import RegexValidator, MinLengthValidator

mobile_validators = [
    RegexValidator(regex='^.{12}$', message='Length has to be 12', code='length12'),
    RegexValidator(regex='^(98)(\d{10})$', message='Country Code should be allowed', code='CountryCode'),
    MinLengthValidator(12, message="It should be at least 12 chars")
]
