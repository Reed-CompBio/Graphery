from django.db import models

from .mixins import PublishedMixin, TimeDateMixin
from .models import User, Tutorial


class ZHCN(PublishedMixin, TimeDateMixin, models.Model):
    # meta
    translator = models.ManyToManyField(User)
    tutorial = models.OneToOneField(Tutorial, on_delete=models.CASCADE)
    # content
    content_md = models.TextField()
    content_html = models.TextField()
