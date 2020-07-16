from typing import Callable, Iterable

from django.db.transaction import commit, rollback
from prompt_toolkit import prompt, print_formatted_text

from cli_utils.cli_ui import new_session
from cli_utils.intel_wrappers.intel_wrapper import AbstractWrapper


@new_session('confirmation')
def proceed_prompt(actions: Callable) -> None:
    proceed = prompt('Proceed Saving? (y/N) ')
    if proceed.lower() == 'y':
        actions()
        commit()
        print_formatted_text('Changes committed.')
    else:
        print_formatted_text('Changes not saved. Rolling back.')
        rollback()
        print_formatted_text('Rolled back')


@new_session('publish confirmation')
def proceed_publishing_content(published_model_wrapper: AbstractWrapper) -> None:
    publish = prompt(f'Publish {published_model_wrapper}? (y/N) ')
    if publish.lower() == 'y':
        published_model_wrapper.model.is_published = True
        published_model_wrapper.model.save()
        commit()
        print_formatted_text('Published Content')
    else:
        print_formatted_text(f'Content {published_model_wrapper} is saved but not published')


def proceed_publishing_content_iter(published_model_wrappers: Iterable[AbstractWrapper]) -> None:
    for published_model_wrapper in published_model_wrappers:
        proceed_publishing_content(published_model_wrapper)
