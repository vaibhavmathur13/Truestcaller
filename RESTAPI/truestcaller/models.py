from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

from truestcaller import constants as truestcaller_constants


class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """
    Define a model manager for User model with no username field.
    """
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """
        Create and save a User with the given phone number and password.
        """
        if not phone_number:
            raise ValueError('Phone number is required')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser, BaseClass):
    """
    This model contains Registered User information with the required fields
    """
    username = None
    name = models.CharField(_('name'), max_length=truestcaller_constants.NAME_MAX_LENGTH, blank=False, null=False)
    phone_number = models.CharField(validators=[truestcaller_constants.PHONE_REGEX],
                                    unique=True, max_length=truestcaller_constants.PHONE_MAX_LENGTH)
    email = models.EmailField(_('email address'), unique=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return '%s %s' % (self.name, self.phone_number)


class Directory(BaseClass):
    """
    This model contains Global database for all Phone numbers
    """
    added_by = models.ForeignKey(User, related_name='contact_list', on_delete=models.CASCADE, null=True)
    name = models.CharField(_('name'), max_length=truestcaller_constants.NAME_MAX_LENGTH, blank=True)
    phone_number = models.CharField(validators=[truestcaller_constants.PHONE_REGEX],
                                    max_length=truestcaller_constants.PHONE_MAX_LENGTH)
    is_spam = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.name, self.phone_number)
