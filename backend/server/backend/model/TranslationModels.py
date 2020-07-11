from typing import Type, TypeVar

from django.db import models

from .mixins import PublishedMixin, TimeDateMixin, UUIDMixin
from .UserModel import User
from .TutorialRelatedModel import Tutorial, Graph, FAKE_UUID

from .translation_collection import add_trans_table, add_graph_info_trans_table


NULL_CONTENT_TITLE = '<None>'


class TranslationBase(PublishedMixin, TimeDateMixin, UUIDMixin, models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False, null=False, db_index=True)
    # meta
    authors = models.ManyToManyField(User)
    tutorial_anchor = models.OneToOneField(Tutorial, on_delete=models.CASCADE)
    abstract = models.TextField()
    # content
    content_md = models.TextField()
    content_html = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return f'<{type(self).__name__}_translation {self.title} | {self.abstract[:100]}>'


@add_trans_table
class ENUS(TranslationBase):
    class Meta:
        verbose_name = 'EN-US translation'


@add_trans_table
class ZHCN(TranslationBase):
    class Meta:
        verbose_name = 'ZH-CN translation'


class GraphTranslationBase(PublishedMixin, TimeDateMixin, UUIDMixin, models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False, null=False)
    abstract = models.TextField()
    graph_anchor = models.OneToOneField(Graph, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f'<{type(self).__name__}_graph_content {self.title} | {self.abstract[:100]}>'


@add_graph_info_trans_table
class ENUSGraphContent(GraphTranslationBase):
    pass


@add_graph_info_trans_table
class ZHCNGraphContent(GraphTranslationBase):
    pass


T = TypeVar("T")


def make_dummy_content(content_model: Type[T]) -> T:
    return content_model(id=FAKE_UUID,
                         title=NULL_CONTENT_TITLE,
                         abstract='This is a empty Anchor. No translation exists.',
                         is_published=False)


def make_dummy_tutorial_content() -> TranslationBase:
    return make_dummy_content(ENUS)


def make_dummy_graph_content() -> GraphTranslationBase:
    return make_dummy_content(ENUSGraphContent)
