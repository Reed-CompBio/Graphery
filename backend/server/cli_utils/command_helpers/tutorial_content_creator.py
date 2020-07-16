import pathlib
from typing import List, Optional, Tuple, Type

import markdown
from bs4 import BeautifulSoup, Tag, ResultSet
from prompt_toolkit import print_formatted_text

from backend.model.TranslationModels import TranslationBase
from cli_utils.cli_ui import run_interruptable_checkbox_dialog, info_session
from cli_utils.command_helpers.command_base import CommandBaseOverIterable
from cli_utils.controller_helpers.prompt_consent import proceed_publishing_content_iter, proceed_prompt
from cli_utils.controller_helpers.prompt_getters import get_location, get_name, get_abstract
from cli_utils.controller_helpers.prompt_selectors import select_tutorial_lang, select_authors, select_tutorial
from cli_utils.intel_wrapper import TutorialTranslationContentWrapper, finalize_prerequisite_wrapper_iter


class TutorialContentCreator(CommandBaseOverIterable):

    def gather_info(self) -> None:
        pass

    def output_created_confirmation_info(self) -> None:
        pass

    def output_not_created_confirmation_info(self) -> None:
        pass

    def create(self) -> bool:
        pass

    def proceed_helper(self) -> None:
        pass


def get_locale_md_files() -> List[pathlib.Path]:
    source_folder: pathlib.Path = get_location(prompt_text='Please choose the tutorial translation folder')
    md_file_paths: List[pathlib.Path] = [path for path in source_folder.glob('*.md')]

    md_selection_values = [(element, element.name) for element in md_file_paths]

    selected_graph_file_paths = run_interruptable_checkbox_dialog(
        text='Please select the translations you want to upload',
        values=md_selection_values,
        default_values=md_selection_values
    )
    return selected_graph_file_paths


def get_html_soup_from_string(html_string: str) -> BeautifulSoup:
    return BeautifulSoup(html_string, 'html.parser')


def get_img_file(parent_folder: pathlib.Path, img_tag: Tag) -> Optional[pathlib.Path]:
    file_name = img_tag.get('src', None)
    if file_name:
        return parent_folder / file_name
    return None


def move_file_to_static_folder(file: pathlib.Path, static_folder: pathlib.Path, target_folder: pathlib.Path) -> None:
    pass


def process_images(soup: BeautifulSoup, html_parent_folder: pathlib.Path) -> None:
    img_tags: ResultSet = soup.find_all('img')
    for img_tag in img_tags:
        img_file_path = get_img_file(html_parent_folder, img_tag)
        if not img_file_path:
            continue
        # TODO finish this
        # move_file_to_static_folder(img_file_path,)


def parse_markdown(text: str) -> BeautifulSoup:
    result: str = markdown.markdown(text, extensions=['codehilite', 'md_in_html', 'markdown_del_ins',
                                                      'pymdownx.arithmatex', 'pymdownx.details',
                                                      'pymdownx.inlinehilite', 'pymdownx.superfences'])
    soup = get_html_soup_from_string(result)

    return soup
    # TODO add arithmatex required js to the page


def get_meta_info_from_html(soup: BeautifulSoup) -> Tuple[str, str, str]:
    title = soup.h1.text
    soup.h1.decompose()
    content_html = str(soup)
    abstract = str(soup.p)
    return title, content_html, abstract


def gather_locale_md_info(path: pathlib.Path) -> TutorialTranslationContentWrapper:
    try:
        name_and_lang = path.stem.split('.')
        if len(name_and_lang) < 2:
            name, = name_and_lang
            lang = 'en-us'
        elif len(name_and_lang) > 2:
            raise
        else:
            name, lang = name_and_lang
        # TODO I don't think you can do much about it since you can't change the input source in the command line?
        # TODO this is broken because when the lang is not specified, it just returns None
        lang_class: Type[TranslationBase] = select_tutorial_lang(lang)

        content_md = path.read_text()
        soup = parse_markdown(text=content_md)

        md_title, content_html, abstract = get_meta_info_from_html(soup)

        process_images(soup, path.absolute().parent)
        # TODO there is a new line in str(soup)

        title: str = get_name(message='Please edit the title of this tutorial:',
                              default=md_title if md_title else name)

        # TODO again, you can't do much in a command line I guess?
        abstract: str = get_abstract(message='Edit the abstract of this translation:', default=abstract)

        authors = select_authors()
        tutorial_anchor = select_tutorial()

        return TutorialTranslationContentWrapper().set_variables(
            model_class=lang_class,
            title=title,
            authors=authors,
            tutorial_anchor=tutorial_anchor,
            abstract=abstract,
            content_md=content_md,
            content_html=content_html
        )

    except ValueError as e:
        e.args = ('Please follow the naming convention',)


def gather_md_files(md_file_paths: List[pathlib.Path]) -> List[TutorialTranslationContentWrapper]:
    return [gather_locale_md_info(path) for path in md_file_paths]


def create_locale_md() -> None:
    md_paths = get_locale_md_files()
    if not md_paths:
        print_formatted_text('Nothing is selected. Exiting')
        return
    md_file_wrappers = gather_md_files(md_paths)

    # TODO the incorporate edit mode. In the current frame work, this will just load the model from the database
    #  if it's already in there and does basically nothing to it. You should show a warning for now and
    #  and a edit option to it later. Same as for graphs.

    info_session()
    print_formatted_text('The following translations are created: ')
    for wrapper in md_file_wrappers:
        print_formatted_text(f'{wrapper}')

    def actions():
        finalize_prerequisite_wrapper_iter(md_file_wrappers)

        proceed_publishing_content_iter(md_file_wrappers)

    proceed_prompt(actions=actions)

