import pathlib
from typing import List, Optional

import bs4
from prompt_toolkit import print_formatted_text

from cli_utils.cli_ui import run_interruptable_checkbox_dialog

from cli_utils.command_helpers.command_base import CommandBaseOverIterable

from cli_utils.controller_helpers.content_creator_helper import get_file_name_and_lang, parse_markdown, \
    get_title_from_soup, get_abstract_from_soup, get_content_from_soup
from cli_utils.controller_helpers.prompt_consent import proceed_publishing_content_iter
from cli_utils.controller_helpers.prompt_getters import get_location, get_name, get_abstract
from cli_utils.controller_helpers.prompt_selectors import select_tutorial_lang, select_authors, select_tutorial

from cli_utils.intel_wrappers.intel_wrapper import TutorialTranslationContentWrapper, finalize_prerequisite_wrapper_iter


class TutorialContentCreator(CommandBaseOverIterable):
    def __init__(self):
        super(TutorialContentCreator, self).__init__('Create Tutorial Content')
        self.tutorial_content_wrappers = []

    @staticmethod
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

    @staticmethod
    def get_file_from_src(parent_folder: pathlib.Path, img_tag: bs4.Tag) -> Optional[pathlib.Path]:
        file_name: Optional[str] = img_tag.get('src')
        if file_name:
            return parent_folder / file_name
        return None

    @staticmethod
    def move_file_to_static_folder(file: pathlib.Path, static_folder: pathlib.Path,
                                   target_folder: pathlib.Path) -> None:
        # TODO
        pass

    @staticmethod
    def rewrite_src_path(src: pathlib.Path, static_folder: pathlib.Path) -> None:
        pass

    @staticmethod
    def process_images(soup: bs4.BeautifulSoup,
                       html_parent_folder: pathlib.Path,
                       url: str) -> None:

        img_tags: bs4.ResultSet = soup.find_all('img')
        video_tags: bs4.ResultSet = soup.find_all('video')
        audio_tags: bs4.ResultSet = soup.find_all('audio')
        source_tags: bs4.ResultSet = soup.find_all('source')

        for src_tag in img_tags:
            img_file_path = TutorialContentCreator.get_file_from_src(html_parent_folder, src_tag)
            if not img_file_path:
                # TODO
                raise

            if not img_file_path.exists():
                # TODO warn users
                raise

            TutorialContentCreator.move_file_to_static_folder()

    def gather_locale_md_info(self, path: pathlib.Path) -> None:
        self.new_attr()

        try:
            name, lang = get_file_name_and_lang(path.stem)

            # TODO I don't think you can do much about it since you can't change the input source in the command line?
            # TODO this is broken because when the lang is not specified, it just returns None
            self.set_attr('model_class', select_tutorial_lang(lang))

            content_md = path.read_text()
            # TODO think about positioning
            self.set_attr('content_md', content_md)

            soup: bs4.BeautifulSoup = parse_markdown(text=content_md)

            html_title = get_title_from_soup(soup)
            html_abstract = get_abstract_from_soup(soup)

            # TODO there is a new line in str(soup)

            self.set_attr('title', get_name(message='Please edit the title of this tutorial:',
                                            default=html_title if html_title else name))

            anchor = select_authors()

            TutorialContentCreator.process_images(soup, path.absolute().parent)

            # TODO again, you can't do much in a command line I guess?
            self.set_attr('abstract',
                          get_abstract(message='Edit the abstract of this translation:', default=html_abstract))

            self.set_attr('content_html', get_content_from_soup(soup))
            self.set_attr('authors', anchor)
            self.set_attr('tutorial_anchor', select_tutorial())

        except ValueError as e:
            e.args = ('Please follow the naming convention',)
            # TODO
            raise

    def gather_info(self) -> None:
        locale_md_files = self.get_locale_md_files()

        print_formatted_text('The tutorial content md files found: ')
        for path in locale_md_files:
            print_formatted_text('  {}'.format(path.absolute()))

        for path in locale_md_files:
            try:
                self.gather_locale_md_info(path)
            except Exception as e:
                deleted_ele = self.del_attr()
                e.args = (f'Exception occurs when creating a tutorial content: {deleted_ele}. Error: {e}',)
                # TODO
                raise

    def output_created_confirmation_info(self) -> None:
        print_formatted_text('The following translations are created: ')
        for wrapper in self.tutorial_content_wrappers:
            print_formatted_text(f'{wrapper}')

    def output_not_created_confirmation_info(self) -> None:
        print_formatted_text('No tutorial conent is created')

    def create(self) -> bool:
        self.tutorial_content_wrappers.extend(TutorialTranslationContentWrapper().set_variables(**info_dict)
                                              for info_dict in self.command_attrs)

        return not not self.tutorial_content_wrappers

    def proceed_helper(self) -> None:
        finalize_prerequisite_wrapper_iter(self.tutorial_content_wrappers)
        proceed_publishing_content_iter(self.tutorial_content_wrappers)
