from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeDateMixin, PublishedMixin, UUIDMixin
from .translation_collection import process_trans_name


class Category(UUIDMixin, PublishedMixin, models.Model):
    category = models.CharField(max_length=50, unique=True,
                                default=_('uncategorized'), blank=False, null=False)


class Tutorial(UUIDMixin, PublishedMixin, TimeDateMixin, models.Model):
    # meta data
    # TODO add a url verification
    url = models.CharField(max_length=100, unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    categories = models.ManyToManyField(Category)

    def get_translation(self, translation: str, default: str):
        return getattr(self,
                       process_trans_name(translation),
                       getattr(self, process_trans_name(default), None))


class GraphPriority(models.IntegerChoices):
    MAIN = 60, 'Main Graph'
    SUPP = 40, 'Supplement Graph'
    TRIV = 20, 'Trivial Graph'


class Graph(UUIDMixin, PublishedMixin, TimeDateMixin, models.Model):
    url = models.CharField(max_length=100, unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    graph_info = models.TextField()
    priority = models.PositiveSmallIntegerField(choices=GraphPriority.choices, default=GraphPriority.MAIN)
    # json
    cyjs = JSONField()
    # belongs to
    tutorials = models.ManyToManyField(Tutorial)


class Code(UUIDMixin, TimeDateMixin, models.Model):
    # relations
    # TODO I suppose this should a one-to-one field.
    tutorial = models.OneToOneField(Tutorial, on_delete=models.CASCADE)
    # content
    # TODO unique necessary? or unique together with tutorial? Unique for now.
    code = models.TextField(unique=True)

    @property
    def is_published(self) -> bool:
        return self.tutorial.is_published


class ExecResultJson(UUIDMixin, TimeDateMixin, models.Model):
    # relations
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    # content
    json = JSONField()

    @property
    def is_published(self) -> bool:
        """
        the code execution result is published when the
        tutorial and the graph are both published
        @return:
        """
        return self.code.is_published and self.graph.is_published

    class Meta:
        # serves as unique together
        constraints = [
            models.UniqueConstraint(fields=['code', 'graph'], name='code exec result constraint')
        ]
