from typing import Tuple, Sequence, List, TypeVar

from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Label, CheckboxList, Box
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.dimension import Dimension as d


def inline_checkbox_dialog(text: str = '',
                           values: Sequence[Tuple] = (),
                           default_values: Sequence[Tuple] = (),
                           additional_helper_text: Sequence[Label] = (),
                           style=None):
    bindings = KeyBindings()

    cb_list = CheckboxList(values)
    for default_value in default_values:
        cb_list.current_values.append(default_value[0])

    @bindings.add('c-e')
    def ok_handler(event: KeyPressEvent) -> None:
        event.app.exit(result=cb_list.current_values)

    @bindings.add('c-c')
    def cancel_handler(event: KeyPressEvent) -> None:
        event.app.exit()

    helper_label = Label('Press <space> or <enter> to select. Press <ctrl+e> to confirm.')
    content = Label(text)

    # noinspection PyTypeChecker
    application = Application(
        layout=Layout(HSplit([
            Box(
                body=HSplit([
                    helper_label,
                    *additional_helper_text,
                    content,
                ]),
                padding_top=1,
                padding_left=0,
                padding_right=0

            ),
            Box(
                body=cb_list,
                padding=d(preferred=1, max=1)
            )
        ])),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=False)

    return application


T = TypeVar("T")


def interruptable_checkbox_dialog(text: str = '',
                                  values: Sequence[Tuple[T, AnyFormattedText]] = (),
                                  default_values: Sequence[Tuple] = (),
                                  additional_helper_text: Sequence[Label] = (),
                                  style=None) -> List[T]:
    result = inline_checkbox_dialog(text=text,
                                    values=values,
                                    default_values=default_values,
                                    additional_helper_text=additional_helper_text,
                                    style=style).run()
    if result is None:
        raise KeyboardInterrupt

    return result
