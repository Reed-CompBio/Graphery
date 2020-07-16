from typing import Optional

from django.db.models import QuerySet
from prompt_toolkit import print_formatted_text

from backend.model.TutorialRelatedModel import Tutorial

from cli_utils.command_helpers.command_base import CommandBase

from cli_utils.controller_helpers.cli_validators import name_validator, url_validator
from cli_utils.controller_helpers.prompt_consent import proceed_publishing_content
from cli_utils.controller_helpers.prompt_getters import get_name, get_url
from cli_utils.controller_helpers.prompt_selectors import select_and_add_categories

from cli_utils.intel_wrappers.intel_wrapper import TutorialAnchorWrapper, finalize_prerequisite_wrapper


class TutorialAnchorCreator(CommandBase):
    def __init__(self):
        super().__init__('Create/Overwrite Anchor')
        self.tutorialAnchorWrapper: Optional[TutorialAnchorWrapper] = None

    def gather_info(self):
        tutorial_query_set: QuerySet = Tutorial.objects.all()

        print_formatted_text('For naming convention, please visit https://poppy-poppy.github.io/Graphery/')

        name = self.set_attr('name',
                             get_name(message='Please enter the name of the tutorial: ',
                                      validator=name_validator(tutorial_query_set)))

        self.set_attr('url', get_url(message='Please enter the url of the tutorial: ',
                                     validator=url_validator(tutorial_query_set),
                                     default=name))

        self.set_attr('categories', select_and_add_categories())

    def create(self) -> bool:
        self.tutorialAnchorWrapper = TutorialAnchorWrapper().set_variables(**self.command_attrs)
        return True

    def output_created_confirmation_info(self) -> None:
        print_formatted_text('Tutorial anchor created')
        print_formatted_text('name: {}'.format(self.tutorialAnchorWrapper.name))
        print_formatted_text('url: {}'.format(self.tutorialAnchorWrapper.url))
        print_formatted_text('categories: {}'.format(self.tutorialAnchorWrapper.categories))

    def output_not_created_confirmation_info(self) -> None:
        print_formatted_text('Tutorial anchor not created')

    def proceed_helper(self):
        finalize_prerequisite_wrapper(self.tutorialAnchorWrapper)
        proceed_publishing_content(self.tutorialAnchorWrapper)
