from typing import Tuple, Sequence, List, TypeVar, Callable

from prompt_toolkit import print_formatted_text
from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Label, CheckboxList, Box, RadioList
from prompt_toolkit.layout.containers import HSplit


def new_session(session_text: str = '') -> Callable:
    def wrapper_gen(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            print_formatted_text('\n======= {} ======='.format(session_text))
            return func(*args, **kwargs)

        return wrapper

    return wrapper_gen


def make_separation(session_text: str) -> None:
    new_session(session_text)(lambda: None)()


def gen_application(text: str,
                    additional_helper_text: Sequence[str] = (),
                    body=None,
                    bindings: KeyBindings = None,
                    style=None) -> Application:
    helper_label = Label('Press <space> or <enter> to select. Press <ctrl+e> to confirm.')
    content = Label(text)

    # noinspection PyTypeChecker
    return Application(
        layout=Layout(HSplit([
            Box(
                body=HSplit([
                    helper_label,
                    *map(lambda x: Label(x), additional_helper_text),
                    content,
                ]),
                padding_left=0,
                padding_right=0

            ),
            Box(
                body=body,
                padding_left=1,
                padding_right=0
            )
        ])),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style)


def _inline_checkbox_dialog(text: str = '',
                            values: Sequence[Tuple] = (),
                            default_values: Sequence[Tuple] = (),
                            additional_helper_text: Sequence[str] = (),
                            style=None) -> Application:
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

    application = gen_application(text=text,
                                  additional_helper_text=additional_helper_text,
                                  body=cb_list,
                                  bindings=bindings,
                                  style=style)

    return application


def _inline_radio_dialog(text: str = '',
                         values: Sequence[Tuple] = (),
                         default_value: Tuple = (),
                         additional_helper_text: Sequence[str] = (),
                         style=None) -> Application:
    bindings = KeyBindings()

    @bindings.add('c-c')
    def exit_(event):
        event.app.exit(result=None)

    @bindings.add('c-e')
    def exit_with_value(event):
        event.app.exit(result=radio_list.current_value)

    radio_list = RadioList(values=values)
    if default_value:
        radio_list.current_value = default_value[0]

    application = gen_application(text=text,
                                  additional_helper_text=additional_helper_text,
                                  body=radio_list,
                                  bindings=bindings,
                                  style=style)

    return application


_G = TypeVar("_G")


def run_interruptable_checkbox_dialog(text: str = '',
                                      values: Sequence[Tuple[_G, AnyFormattedText]] = (),
                                      default_values: Sequence[Tuple] = (),
                                      additional_helper_text: Sequence[str] = (),
                                      style=None) -> List[_G]:
    result = _inline_checkbox_dialog(text=text,
                                     values=values,
                                     default_values=default_values,
                                     additional_helper_text=additional_helper_text,
                                     style=style).run()
    if result is None:
        raise KeyboardInterrupt

    return result


_K = TypeVar("_K")


def run_interruptable_radio_box_dialog(text: str = '',
                                       values: Sequence[Tuple[_K, AnyFormattedText]] = (),
                                       default_value: Tuple = (),
                                       additional_helper_text: Sequence[str] = (),
                                       style=None) -> _K:
    result: _K = _inline_radio_dialog(text=text,
                                      values=values,
                                      default_value=default_value,
                                      additional_helper_text=additional_helper_text,
                                      style=style).run()
    if result is None:
        raise KeyboardInterrupt

    return result
