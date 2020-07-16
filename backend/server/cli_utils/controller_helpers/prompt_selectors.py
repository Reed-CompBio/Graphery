from typing import List, Tuple

from django.db.models import QuerySet

from backend.model.UserModel import ROLES
from backend.model.translation_collection import translation_table_mapping, get_translation_table, \
    get_graph_info_trans_table

from cli_utils.cli_ui import new_session, run_interruptable_checkbox_dialog, run_interruptable_radio_box_dialog
from .prompt_getters import new_line_prompt

from cli_utils.intel_wrappers.intel_wrapper import *


@new_session('select and add categories')
def select_and_add_categories() -> List[CategoryWrapper]:
    category_query_set: QuerySet = Category.objects.all()
    category_selections: List[Tuple[Category, str]] = [(model, model.category) for model in category_query_set]

    category_choices: List[Category] = run_interruptable_checkbox_dialog(
        text='Please choose existing categories: ',
        values=category_selections
    )

    new_categories: Iterable[str] = map(
        lambda x: x.strip(),
        new_line_prompt(message='Please enter new categories. Separate with ";"').split(';')
    )

    return [CategoryWrapper().load_model(category_model)
            for category_model in category_choices if category_model] + \
           [CategoryWrapper().set_variables(category_name=category_name)
            for category_name in new_categories if category_name]


@new_session('select authors')
def select_authors() -> List[UserWrapper]:
    user_query_set: QuerySet = User.objects.all()
    user_selections: List[Tuple[User, str]] = [(model, f'{model.username}: {model.email}') for model in user_query_set]

    user_choices: List[User] = run_interruptable_checkbox_dialog(
        text='Please choose authors: ',
        values=user_selections
    )

    return [UserWrapper().load_model(user_model) for user_model in user_choices if user_model]


@new_session('select graph priority')
def select_graph_priority() -> int:
    return int(run_interruptable_radio_box_dialog(text='Please select the priority of this graph',
                                                  values=[(60, 'major graph',),
                                                          (40, 'minor graph',),
                                                          (20, 'trivial graph')]))


@new_session('select matching tutorials')
def select_tutorials() -> List[TutorialAnchorWrapper]:
    tutorial_query_set = Tutorial.objects.all()
    tutorial_selections = [(model, f'{model.url}: {model.name}') for model in tutorial_query_set]

    tutorial_choices: List[Tutorial] = run_interruptable_checkbox_dialog(
        text='Please select tutorials',
        values=tutorial_selections
    )

    return [TutorialAnchorWrapper().load_model(tutorial_model) for tutorial_model in tutorial_choices if tutorial_model]


@new_session('select matching tutorial')
def select_tutorial() -> TutorialAnchorWrapper:
    tutorial_query_set = Tutorial.objects.all()
    tutorial_selections = [(model, f'{model.url}: {model.name}') for model in tutorial_query_set]

    tutorial_choice: Tutorial = run_interruptable_radio_box_dialog(
        text='Please select a tutorial',
        values=tutorial_selections
    )

    return TutorialAnchorWrapper().load_model(tutorial_choice)


@new_session('select tutorial language')
def select_tutorial_lang(default_lang: str = 'en-us') -> Type[TranslationBase]:
    lang_selections: List[Tuple[Type[TranslationBase], str]] = \
        [(cls, f'{lang[:2]}-{lang[2:]}') for lang, cls in translation_table_mapping.items()]

    lang_choice: Type[TranslationBase] = run_interruptable_radio_box_dialog(
        text='Please select the language',
        values=lang_selections,
        default_value=(get_translation_table(default_lang), default_lang)
    )
    return lang_choice


@new_session('select graph language')
def select_graph_lang(default_lang: str = 'en-us') -> Type[GraphTranslationBase]:
    lang_selections: List[Tuple[Type[GraphTranslationBase], str]] = \
        [(cls, f'{lang[:2]}-{lang[2:4]}') for lang, cls in translation_table_mapping.items()]

    lang_choice: Type[GraphTranslationBase] = run_interruptable_radio_box_dialog(
        text='Please select language',
        values=lang_selections,
        default_value=(get_graph_info_trans_table(default_lang), default_lang)
    )
    return lang_choice


@new_session('select graph')
def select_graph() -> GraphWrapper:
    graph_query_set: QuerySet = Graph.objects.all()
    graph_selections: List[Tuple[Graph, str]] = [(graph_model, f'{graph_model.url}: {graph_model.name}')
                                                 for graph_model in graph_query_set]

    graph_choices: Graph = run_interruptable_radio_box_dialog(
        text='Please select the matching graph',
        values=graph_selections,
    )

    return GraphWrapper().load_model(graph_choices)


@new_session('select user role')
def select_role() -> int:
    role_selection: int = run_interruptable_radio_box_dialog(
        text='Please select the role of this user',
        values=[
            (value, label) for value, label in ROLES.choices
        ],
        default_value=(ROLES.VISITOR, '')
    )

    return role_selection
