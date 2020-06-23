from typing import Tuple
from uuid import uuid4

from django.db import models
from django.db.models import QuerySet
from graphql import ResolveInfo

from backend.model.filters import published_filter


class TimeDateMixin(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishedMixin(models.Model):
    # TODO make it true for now
    is_published = models.BooleanField(default=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class FilterMixin(models.Model):
    _universal_editor = [published_filter]
    filters = []

    @classmethod
    def filtered_queryset(cls,
                          info: ResolveInfo = None
                          ) -> QuerySet:
        raw_queryset = cls.objects.all()
        for single_filter in cls.filters + cls._universal_editor:
            raw_queryset = single_filter(raw_queryset, info)
        return raw_queryset

    class Meta:
        abstract = True


def field_adder(extra_fields: Tuple):
    def wrapper(cls):
        cls.fields += extra_fields
        return cls

    return wrapper


time_date_mixin_field = ('created_time', 'modified_time')

time_date_field_adder = field_adder(time_date_mixin_field)

published_mixin_field = ('is_published',)

published_field_adder = field_adder(published_mixin_field)

uuid_mixin_field = ('id',)

uuid_field_adder = field_adder(uuid_mixin_field)
