from typing import Callable, Optional
from os.path import join

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.conf import settings

from .UserModel import User
from .mixins import PublishedMixin, TimeDateMixin, UUIDMixin
from .translation_collection import process_trans_name, process_graph_info_trans_name


FAKE_UUID = '00000000-0000-0000-0000-000000000000'


class Category(PublishedMixin, UUIDMixin, models.Model):
    category = models.CharField(max_length=50, unique=True,
                                default='uncategorized', blank=False, null=False)

    def __str__(self):
        return f'<category {self.category}>'

    class Meta:
        verbose_name_plural = 'categories'


class Tutorial(PublishedMixin, UUIDMixin, TimeDateMixin, models.Model):
    # meta data
    # TODO add a url verification
    url = models.CharField(max_length=100, unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    categories = models.ManyToManyField(Category, default='uncategorized')

    dummy_content_gen: Optional[Callable[[], models.Model]] = None

    @classmethod
    def default_dummy_content(cls) -> models.Model:
        if cls.dummy_content_gen is None:
            from .TranslationModels import make_dummy_tutorial_content
            cls.dummy_content_gen = make_dummy_tutorial_content
        return cls.dummy_content_gen()

    def get_translation(self, translation: str, default: str, is_published_only: bool = True):
        content = getattr(self,
                          process_trans_name(translation),
                          getattr(self, process_trans_name(default), None))
        if content:
            if content.is_published or not is_published_only:
                return content
        # TODO this is not dry enough

        return Tutorial.default_dummy_content()

    def __str__(self):
        return f'<tutorial {self.url} | {self.name}>'


class GraphPriority(models.IntegerChoices):
    MAIN = 60, 'Main Graph'
    SUPP = 40, 'Supplement Graph'
    TRIV = 20, 'Trivial Graph'


class Graph(PublishedMixin, TimeDateMixin, UUIDMixin, models.Model):
    url = models.CharField(max_length=100, unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    categories = models.ManyToManyField(Category, default='uncategorized')
    authors = models.ManyToManyField(User)
    priority = models.PositiveSmallIntegerField(choices=GraphPriority.choices, default=GraphPriority.MAIN)
    # json
    cyjs = JSONField()
    # belongs to
    tutorials = models.ManyToManyField(Tutorial)

    dummy_content_gen: Optional[Callable[[], models.Model]] = None

    @classmethod
    def default_dummy_content(cls) -> models.Model:
        if cls.dummy_content_gen is None:
            from .TranslationModels import make_dummy_graph_content
            cls.dummy_content_gen = make_dummy_graph_content
        return cls.dummy_content_gen()

    def get_translation(self, translation: str, default: str, is_published_only: bool = True):
        content = getattr(self,
                          process_graph_info_trans_name(translation),
                          getattr(self, process_graph_info_trans_name(default), None))
        if content:
            if content.is_published or not is_published_only:
                return content

        return Graph.default_dummy_content()

    def __str__(self):
        return f'<graph {self.url} | {self.name} | {GraphPriority(self.priority).label}>'


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

    def __str__(self):
        return f'<code {self.tutorial} | {self.code[:100]}>'


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

    def __str__(self):
        return f'<exec result json {self.code} | {self.graph}>'


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/MEDIA_FOLDER_NAME/<tutorial_name>_<tutorial_id>/<filename>
    return join(settings.MEDIA_FOLDER_NAME,
                f'{instance.link_id}',
                filename)


class UploadWhere(models.TextChoices):
    TUTORIAL = ('TR', 'Tutorial')
    GRAPH = ('GR', 'Graph')


class Uploads(PublishedMixin, UUIDMixin, models.Model):
    where = models.CharField(max_length=2, choices=UploadWhere.choices, default=UploadWhere.TUTORIAL)
    link_id = models.UUIDField(blank=False, null=False)
    file = models.FileField(upload_to=user_directory_path)
