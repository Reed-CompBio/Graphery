from uuid import uuid4

from django.db import models


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


time_date_mixin_field = ('created_time', 'modified_time')


published_mixin_field = ('is_published', )


uuid_mixin_field = ('id', )
