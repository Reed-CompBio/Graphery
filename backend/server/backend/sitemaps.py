from typing import List

from django.contrib.sitemaps import Sitemap
from django.db.models import QuerySet

from backend.model.translation_collection import translation_tables, graph_info_translation_tables
from backend.models import Tutorial, Graph


class FakeSite:
    def __init__(self):
        self.domain = 'graphery.reedcompbio.org'
        self.name = 'graphery.reedcompbio.org'


static_pages = ['', '/tutorials', '/graphs', '/about', ]


def get_trans_url(trans: str) -> str:
    return f'{trans[0:2]}-{trans[2:4]}'


def get_content_link(queryset: QuerySet, trans_collection: List[str], prefix: str):
    for trans in trans_collection:
        trans_url: str = get_trans_url(trans)
        for element in queryset:
            trans_model = getattr(element, trans, None)
            if trans_model is None:
                yield None
            else:
                if trans_model.is_published:
                    yield f'/{prefix}/{trans_url}/{element.url}'
                yield None


def get_model_sites():
    all_tutorials: QuerySet = Tutorial.objects.filter(is_published=True)
    tutorial_url_gen = get_content_link(all_tutorials, translation_tables, 'tutorial')
    all_graphs: QuerySet = Graph.objects.filter(is_published=True)
    graph_url_gen = get_content_link(all_graphs, graph_info_translation_tables, 'graph')

    return [tutorial_url for tutorial_url in tutorial_url_gen if tutorial_url] + \
           [graph_url for graph_url in graph_url_gen if graph_url]


class BackendSitemap(Sitemap):
    def get_urls(self, site=None, **kwargs):
        return super().get_urls(site=FakeSite(),
                                protocol='https')

    def items(self):
        return static_pages + get_model_sites()

    def location(self, item):
        return item
