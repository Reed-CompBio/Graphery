from django.db import models
from django.contrib.auth.models import User


class WebUser(models.Model):
    """
    Extended User in django.
    """
    class ROLES(models.TextChoices):
        ADMINISTRATOR = 'AD', 'Administrator'
        AUTHOR = 'AU', 'author'
        TRANSLATOR = 'TR', 'translator'
        VISITOR = 'VI', 'visitor'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLES.choices, default=ROLES.VISITOR)
