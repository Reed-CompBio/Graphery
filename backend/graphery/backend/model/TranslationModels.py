from django.db import models

from .mixins import PublishedMixin, TimeDateMixin
from .UserModel import User
from .TutorialRelatedModel import Tutorial


class ZHCN(PublishedMixin, TimeDateMixin, models.Model):
    # meta
    translator = models.ManyToManyField(User)
    tutorial = models.OneToOneField(Tutorial, on_delete=models.CASCADE)
    abstract = models.TextField()
    # content
    content_md = models.TextField()
    content_html = models.TextField()
