from typing import Tuple, Callable, Sequence

from backend.intel_wrappers.intel_wrapper import CategoryWrapper
from backend.model.TutorialRelatedModel import Category


def category_wrapper_factory(template: str, num: int) -> Tuple[Callable, Callable]:
    def _maker() -> Sequence[CategoryWrapper]:
        return [
            CategoryWrapper().load_model(
                Category.objects.create(category=template.format(i))
            ) for i in range(num)
        ]

    def _destructor(category_wrappers: Sequence[CategoryWrapper]) -> None:
        for wrapper in category_wrappers:
            wrapper.delete_model()

    return _maker, _destructor
