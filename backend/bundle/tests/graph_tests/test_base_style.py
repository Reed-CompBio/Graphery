from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Type, Callable

import pytest

from GraphObjects.Errors import InvalidStyleCollectionError, InvalidClassCollectionError
from bundle.GraphObjects.Base import Stylable


class StyleTestClass(Stylable):
    def __init__(self, styles, classes):
        super(StyleTestClass, self).__init__(styles, classes)


class DefaultStyleTestClass(Stylable):
    default_styles = [
        {
            'selector': 'sct',
            'property': 'ppt',
            'style': {
                'style_property': 'sppt1',
            }
        },
    ]

    default_classes = [
        'class_1',
        'class_2',
    ]

    def __init__(self, styles, classes,
                 add_default_styles: bool = False, add_default_classes: bool = False,
                 style_validator=lambda _: True, class_validator=lambda _: True):
        super(DefaultStyleTestClass, self).__init__(styles, classes,
                                                    style_validator=style_validator, class_validator=class_validator,
                                                    add_default_styles=add_default_styles,
                                                    add_default_classes=add_default_classes)


def generate_output(styles, classes) -> Mapping:
    return {'styles': styles, 'classes': classes}


@pytest.mark.parametrize('styles, classes, add_default_styles, add_default_classes, result', [
    pytest.param(
        [], (), False, False, generate_output([], []), id='empty style empty class without defaults'
    ),
    pytest.param(
        [], (), True, False, generate_output(DefaultStyleTestClass.default_styles, []),
        id='empty style empty class with default styles'
    ),
    pytest.param(
        [], (), False, True, generate_output([], DefaultStyleTestClass.default_classes),
        id='empty style empty class with default classes'
    ),
    pytest.param(
        [{'selector': 'st2', 'style': {'property': 'ppt'}}], ('cs1', 'cs2'), True, False,
        generate_output([{'selector': 'st2', 'style': {'property': 'ppt'}}] + DefaultStyleTestClass.default_styles,
                        ['cs1', 'cs2']),
        id='style and class with default'
    ),
    pytest.param(
        [{'selector': 'st2', 'style': {'property': 'ppt'}}], ('cs1', 'cs2'), False, False,
        generate_output([{'selector': 'st2', 'style': {'property': 'ppt'}}],
                        ['cs1', 'cs2']),
        id='style and class without default'
    ),
    pytest.param(
        json.dumps([{'selector': 'st2', 'style': {'property': 'ppt'}}]), json.dumps(('cs1', 'cs2')), False, False,
        generate_output([{'selector': 'st2', 'style': {'property': 'ppt'}}],
                        ['cs1', 'cs2']),
        id='string style with default classes and styles'
    ),
    pytest.param(
        json.dumps([{'selector': 'st2', 'style': {'property': 'ppt'}}]), json.dumps(('cs1', 'cs2')), True, True,
        generate_output([{'selector': 'st2', 'style': {'property': 'ppt'}}] + DefaultStyleTestClass.default_styles,
                        ['cs1', 'cs2'] + DefaultStyleTestClass.default_classes)
    )
])
def test_style_injections(styles, classes, add_default_styles, add_default_classes, result):
    instance = DefaultStyleTestClass(styles, classes,
                                     add_default_styles=add_default_styles, add_default_classes=add_default_classes)
    assert result['styles'] == instance.styles
    assert result['classes'] == instance.classes


@pytest.mark.parametrize('style_str, class_str, exception', [
    pytest.param(
        'invalid_json', (), InvalidStyleCollectionError,
        id='invalid style json'
    ),
    pytest.param(
        (), 'invalid_class', InvalidClassCollectionError,
        id='invalid class json'
    ),
])
def test_style_error(style_str: str, class_str: str, exception: Type[Exception]):
    with pytest.raises(ValueError):
        DefaultStyleTestClass(style_str, class_str)


@pytest.mark.parametrize('style_validator, class_validator, exception', [
    pytest.param(lambda _: False, lambda _: True, InvalidStyleCollectionError, id='invalid style'),
    pytest.param(lambda _: True, lambda _: False, InvalidClassCollectionError, id='invalid class'),
])
def test_validator(style_validator: Callable, class_validator: Callable, exception: Type[Exception]):
    with pytest.raises(ValueError):
        DefaultStyleTestClass((), (), style_validator=style_validator, class_validator=class_validator)
