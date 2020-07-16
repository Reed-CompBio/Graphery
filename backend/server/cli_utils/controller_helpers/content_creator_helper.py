from typing import Tuple

import markdown
from bs4 import BeautifulSoup


def get_html_soup_from_string(html_string: str) -> BeautifulSoup:
    return BeautifulSoup(html_string, 'html.parser')


def get_file_name_and_lang(file_stem: str) -> Tuple[str, str]:
    name_and_lang = file_stem.split('.')
    if len(name_and_lang) < 2:
        name, = name_and_lang
        lang = 'en-us'
    elif len(name_and_lang) > 2:
        raise
        # TODO
    else:
        name, lang = name_and_lang

    return name, lang


def parse_markdown(text: str) -> BeautifulSoup:
    result: str = markdown.markdown(text, extensions=['codehilite', 'md_in_html', 'markdown_del_ins',
                                                      'pymdownx.arithmatex', 'pymdownx.details',
                                                      'pymdownx.inlinehilite', 'pymdownx.superfences'])
    soup = get_html_soup_from_string(result)

    return soup
