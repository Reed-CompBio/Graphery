from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserNameValidator(RegexValidator):
    # require the length of the user name be at least 6
    regex = r'^[^0-9][\w-]{4,}[^-_]\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and /-/_ characters.'
        'The length should be at least 6 characters'
        'The username should not start with a number of end with _/-'
    )


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, is_staff, is_superuser, role, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(email=self.normalize_email(email),
                          username=username,
                          # keep this True for now, TODO pass email authentication and then make it True
                          is_active=True,
                          is_verified=True,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          role=role,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, **extra_fields):
        """
        create a user with email, password, and username. Username is required
        @param email:
        @param password:
        @param username:
        @param extra_fields:
        @return:
        """
        is_staff = extra_fields.pop('is_staff', False)
        is_superuser = extra_fields.pop('is_superuser', False)
        the_role = extra_fields.pop('role', ROLES.VISITOR)
        return self._create_user(email=email, username=username,
                                 password=password, is_staff=is_staff,
                                 is_superuser=is_superuser, the_role=the_role,
                                 **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Create a super user with a email, password, and username. Username is required
        @param email:
        @param password:
        @param username:
        @param extra_fields:
        @return:
        """
        return self._create_user(email=email, username=username, password=password,
                                 is_staff=True, is_superuser=True,
                                 role=ROLES.ADMINISTRATOR, **extra_fields)


class ROLES(models.TextChoices):
    ADMINISTRATOR = 'AD', 'Administrator'
    AUTHOR = 'AU', 'author'
    TRANSLATOR = 'TR', 'translator'
    VISITOR = 'VI', 'visitor'


class User(AbstractUser):
    username_validator = UserNameValidator()

    username = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        help_text=_('Required. 100 characters or fewer. Letters, digits and -/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(unique=True, blank=False, null=False, max_length=255,
                              error_messages={
                                  'unique': _("A user with that username already exists."),
                              }, )
    # TODO add email authentication and then change this to False,
    is_verified = models.BooleanField(default=True, help_text=_(
        'Show whether the account is verified'
    ))
    role = models.CharField(max_length=2, choices=ROLES.choices, default=ROLES.VISITOR)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    # A list of the field names that will be prompted for
    # when creating a user via the createsuperuser management command.
    REQUIRED_FIELDS = ('email', )
