from uuid import uuid4

from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeDateMixin, PublishedMixin

from .UserModel import User


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
