from django.core.validators import RegexValidator

PHONE_REGEX = RegexValidator(regex=r'^[6-9]\d{9}$',
                             message="Phone number should start from 6 to 9 and must contain 10 digits.")
NAME_MAX_LENGTH = 50
PHONE_MAX_LENGTH = 10
