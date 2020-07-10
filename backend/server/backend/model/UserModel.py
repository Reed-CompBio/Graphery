from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .mixins import UUIDMixin

from .validators import UserNameValidator

__all__ = ['UserNameValidator', 'ROLES', 'UserManager', 'User']


# User Configurations
class UserManager(BaseUserManager):
    def _create_user(self, username: str, email: str,
                     password: str, is_staff: bool,
                     is_superuser: bool, role: int, **kwargs):
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
                          **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **kwargs):
        """
        create a user with email, password, and username. Username is required
        @param email:
        @param password:
        @param username:
        @param kwargs:
        @return:
        """
        the_role = kwargs.pop('role', ROLES.VISITOR)
        if the_role == ROLES.ADMINISTRATOR:
            is_staff = True,
            is_superuser = True
        else:
            is_staff = kwargs.pop('is_staff', False)
            is_superuser = kwargs.pop('is_superuser', False)
        return self._create_user(username=username, email=email,
                                 password=password, is_staff=is_staff,
                                 is_superuser=is_superuser, role=the_role,
                                 **kwargs)

    def create_superuser(self, username, email, password, **kwargs):
        """
        Create a super user with a email, password, and username. Username is required
        @param email:
        @param password:
        @param username:
        @param kwargs:
        @return:
        """
        return self._create_user(username=username, email=email, password=password,
                                 is_staff=True, is_superuser=True,
                                 role=ROLES.ADMINISTRATOR, **kwargs)

    # I don't need to override get_queryset here since I already override is_anonymous and is_authenticated


class ROLES(models.IntegerChoices):
    ADMINISTRATOR = 60, 'Administrator'
    AUTHOR = 40, 'Author'
    TRANSLATOR = 20, 'Translator'
    VISITOR = 0, 'Visitor'


class User(UUIDMixin, AbstractUser):
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
    role = models.PositiveSmallIntegerField(choices=ROLES.choices, default=ROLES.VISITOR)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    # A list of the field names that will be prompted for
    # when creating a user via the createsuperuser management command.
    REQUIRED_FIELDS = ('email',)

    # TODO add a property field that tells the program what privilege this user has
    # TODO add a deactivate func so that an account can be discarded

    @property
    def is_anonymous(self) -> bool:
        return not self.is_active

    @property
    def is_authenticated(self) -> bool:
        return self.is_active

    def __str__(self):
        return f'<user {self.username} | {ROLES(self.role).label}>'
