from __future__ import annotations
from datetime import date

from django.core.management.utils import get_random_secret_key
from django.db import models

from .UserModel import ROLES
from .mixins import UUIDMixin, TimeDateMixin


class MetaData:
    about = ''
    notification_banner = ''
    notification_card_before = ''
    notification_card_after = ''


class InvitationCodeModel(UUIDMixin, TimeDateMixin):
    class Meta:
        verbose_name = 'Invitation code'
        constraints = [
            models.CheckConstraint(
                check=~(models.Q(expiration_date__isnull=True) & models.Q(expiration_times__isnull=True)),
                name='has expiration date or expiration times'
            )
        ]

    invitation_code = models.CharField(max_length=200, unique=True,
                                       null=False, blank=False,
                                       default=get_random_secret_key)
    expiration_date = models.DateField(blank=True, null=True)
    expiration_times = models.IntegerField(blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLES.choices)

    @property
    def usable(self) -> bool:
        times_flag = not (self.expiration_times is not None and self.expiration_times < 0)
        date_flag = not (self.expiration_date is not None and self.expiration_date < date.today())

        return times_flag and date_flag
