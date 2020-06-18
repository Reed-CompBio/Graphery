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
