from __future__ import annotations

from collections.abc import Mapping, Iterable
from typing import Union, NamedTuple

StyleCollection = Union[str, Iterable[Mapping]]
ClassCollection = Union[str, Iterable[str]]
