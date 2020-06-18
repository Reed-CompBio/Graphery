from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.postgres.fields import JSONField, ArrayField
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeDateMixin, PublishedMixin


# User Configurations
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
    REQUIRED_FIELDS = ('email',)


class Category(models.Model):
    category = models.CharField(max_length=30, unique=True, default=_('unclassified'),
                                blank=False, null=False)


class Tutorial(PublishedMixin, TimeDateMixin, models.Model):
    # primary key is generated automatically
    # meta data
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    url = models.CharField(max_length=50, unique=True, blank=False, null=False)
    authors = models.ManyToManyField(User)
    category = models.ManyToManyField(Category)
    abstract = models.TextField(blank=True)
    # content
    content_md = models.TextField('markdown tutorial')
    content_html = models.TextField('HTML tutorial')


class Graph(PublishedMixin, TimeDateMixin, models.Model):
    # automatically generated primary key
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    url = models.CharField(max_length=50, unique=True, blank=False, null=False)
    graph_info = models.TextField()
    # json
    initial_cyjs = JSONField()
    layouts = ArrayField(JSONField())
    styles = ArrayField(JSONField())
    # belongs to
    tutorial = models.ManyToManyField(Tutorial)


class TutorialCode(TimeDateMixin, models.Model):
    # automatically generated primary key
    # relations
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    # content
    code = models.TextField()

    @property
    def is_published(self):
        return self.tutorial.is_published


class GraphInitialCodeExecResultJson(TimeDateMixin, models.Model):
    # automatically generated primary key
    # relations
    code = models.ForeignKey(TutorialCode, on_delete=models.CASCADE)
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    # content
    json = JSONField()

    @property
    def is_published(self):
        """
        the code execution result is published when the
        tutorial and the graph are both published
        @return:
        """
        return self.code.is_published and self.graph.is_published

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'graph'], name='code exec result constraint')
        ]


# import translations
from .trans_models import *
