import pathlib
from typing import List, Optional

import bs4
from prompt_toolkit import print_formatted_text

from cli_utils.cli_ui import run_interruptable_checkbox_dialog

from cli_utils.command_helpers.command_base import CommandBaseOverIterable

from cli_utils.controller_helpers.content_creator_helper import get_file_name_and_lang, parse_markdown, \
    get_title_from_soup, get_abstract_from_soup
from cli_utils.controller_helpers.prompt_consent import proceed_publishing_content_iter
from cli_utils.controller_helpers.prompt_getters import get_name, get_abstract, get_location
from cli_utils.controller_helpers.prompt_selectors import select_graph_lang, select_graph

from cli_utils.intel_wrappers.intel_wrapper import GraphTranslationContentWrapper, finalize_prerequisite_wrapper_iter


class GraphContentCreator(CommandBaseOverIterable):
    def __init__(self):
        super().__init__('Create/Overwrite Graph Content')
        self.graph_content_wrappers: Optional[List[GraphTranslationContentWrapper]] = []

    @staticmethod
    def get_graph_locale_info_md(parent_folder: pathlib.Path) -> List[pathlib.Path]:
        graph_locale_file_values = [(file, file.name) for file in parent_folder.glob('*.md')]

        graph_locale_files: List[pathlib.Path] = run_interruptable_checkbox_dialog(
            text="Please select the graphs' info you want to upload",
            values=graph_locale_file_values,
            default_values=graph_locale_file_values
        )

        return graph_locale_files

    def gather_graph_content(self, info_file: pathlib.Path):
        self.new_attr()

        try:
            file_name, lang = get_file_name_and_lang(info_file.stem)

            self.set_attr('model_class', select_graph_lang(lang))

            soup: bs4.BeautifulSoup = parse_markdown(info_file.read_text())

            html_title: str = get_title_from_soup(soup)
            html_abstract: str = get_abstract_from_soup(soup)

            self.set_attr('title', get_name(message='Please input the title of this graph',
                                            default=html_title if html_title else file_name))

            self.set_attr('abstract',
                          get_abstract(message='Edit the abstract of this translation', default=html_abstract))

            self.set_attr('graph_anchor', select_graph())

        except Exception as e:
            deleted_ele = self.del_attr()
            e.args = (f'An Exception occurs during creating graph content: {deleted_ele}. Error: {e}', )
            # TODO
            raise

    def gather_info(self) -> None:
        graph_info_location: pathlib.Path = get_location()
        graph_info_md_files: List[pathlib.Path] = GraphContentCreator.get_graph_locale_info_md(graph_info_location)

        for info_file in graph_info_md_files:
            self.gather_graph_content(info_file)

    def output_created_confirmation_info(self) -> None:
        print_formatted_text('Graph info translations: ')
        for wrapper in self.graph_content_wrappers:
            print_formatted_text(f'{wrapper}')

    def output_not_created_confirmation_info(self) -> None:
        print_formatted_text('No Graph info translation is created')

    def create(self) -> bool:
        self.graph_content_wrappers = [GraphTranslationContentWrapper().set_variables(**infos)
                                       for infos in self.command_attrs]
        return not not self.graph_content_wrappers

    def proceed_helper(self) -> None:
        finalize_prerequisite_wrapper_iter(self.graph_content_wrappers)
        proceed_publishing_content_iter(self.graph_content_wrappers)
