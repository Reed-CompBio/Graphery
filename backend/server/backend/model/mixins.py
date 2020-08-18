from typing import Tuple
from uuid import uuid4

from django.db import models


class TimeDateMixin(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishedManager(models.Manager):
    def is_published_only_all(self, is_published_only: bool = True):
        if is_published_only:
            return self.all().filter(is_published=True)
        return self.all()


class PublishedMixin(models.Model):
    # TODO make it true for now
    is_published = models.BooleanField(default=True)

    objects = PublishedManager()

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class LevelMixin(models.Model):
    level = models.PositiveSmallIntegerField(unique=True)
    section = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True


def field_adder(*extra_fields: Tuple):
    def wrapper(cls):
        for fields in extra_fields:
            cls.fields += fields
        return cls

    return wrapper


time_date_mixin_field = ('created_time', 'modified_time')

published_mixin_field = ('is_published',)

uuid_mixin_field = ('id',)
