from abc import abstractmethod, ABC
from typing import Optional, Iterable, Mapping, Callable, Any, Type

from django.db import models, IntegrityError

from backend.model.TranslationModels import TranslationBase, GraphTranslationBase
from backend.model.TutorialRelatedModel import Category, Tutorial, Graph, Code, ExecResultJson
from backend.model.UserModel import User


def dummy_validator(info):
    return info


class IntelWrapperBase(ABC):
    def __init__(self, validators: Mapping[str, Callable]):
        self.validators = validators

    def validate(self):
        for field_name, validator in self.validators.items():
            # TODO change error class
            field = getattr(self, field_name, None)
            if not field:
                raise AssertionError('Cannot file the field {} during validation'
                                     .format(field_name))
            try:
                validator(field_name)
            except AssertionError as e:
                e.args = 'The field {} does not pass the validator and has following error: {}' \
                             .format(field_name, e),
                raise


class ModelWrapperBase(ABC):
    model_class: Optional[Type[models.Model]] = None

    def __init__(self):
        self.model: Optional[models.Model] = None

    def model_exists(self) -> bool:
        return self.model and isinstance(self.model, models.Model)

    @classmethod
    def set_model_class(cls, model_class: Type[models.Model]) -> None:
        cls.model_class = model_class

    def load_model(self, loaded_model: models.Model) -> 'ModelWrapperBase':
        self.model = loaded_model
        return self
        # TODO load override and load all the info to fields

    @abstractmethod
    def retrieve_model(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def make_new_model(self) -> None:
        raise NotImplementedError

    def get_model(self, overwrite: bool = False) -> None:
        if not self.model_class:
            raise AssertionError
        # TODO use other error
        # TODO use get_or_create (write it manually)

    def overwrite_model(self) -> None:
        raise NotImplementedError

    def prepare_model(self) -> None:
        pass

    def finalize_model(self) -> None:
        self.save_model()

    def save_model(self) -> None:
        if self.model_exists():
            try:
                self.model.save()
            except IntegrityError as e:
                raise AssertionError('A exception occurs during saving the model {}. Error: {}'
                                     .format(self.model, e))


class SettableBase(ABC):
    def set_variables(self, **kwargs) -> 'SettableBase':
        return self

    @staticmethod
    def get_var_from_kwargs(kwargs: Mapping, var_name: str) -> Optional[Any]:
        return kwargs.get(var_name, None)


class AbstractWrapper(IntelWrapperBase, ModelWrapperBase, SettableBase, ABC):
    def __init__(self, validators: Mapping[str, Callable]):
        IntelWrapperBase.__init__(self, validators)
        ModelWrapperBase.__init__(self)
        SettableBase.__init__(self)

    def set_variables(self, **kwargs) -> 'AbstractWrapper':
        for field_name in self.validators.keys():
            var = kwargs.get(field_name, None)
            if var:
                setattr(self, field_name, var)

        return self

    def overwrite_model(self) -> None:
        for field in self.validators.keys():
            setattr(self.model, field, getattr(self, field))

    def get_model(self, overwrite: bool = False) -> None:
        try:
            self.validate()
            super().get_model()
        except AssertionError as e:
            e.args = 'Something went wrong when validating variables {} for the model {}. Error: {}' \
                         .format(list(self.validators.keys()), self.model_class, e),
            raise

        try:
            self.retrieve_model()
            if overwrite:
                self.overwrite_model()
        except self.model_class.DoesNotExist:
            self.make_new_model()
        except self.model_class.MultipleObjectsReturned as e:
            # which should never happen
            raise AssertionError('Multiple model instances received with model {} and variables {}. Error: {}'
                                 .format(self.model_class, list(self.validators.keys()), e))

    @staticmethod
    def finalize_prerequisite_wrapper_iter(wrappers: Iterable['AbstractWrapper']):
        for wrapper in wrappers:
            wrapper.get_model()
            wrapper.prepare_model()
            wrapper.finalize_model()


class PublishedWrapper(AbstractWrapper, ABC):
    def __init__(self, validators: Mapping[str, Callable]):
        super(PublishedWrapper, self).__init__(validators)

    def set_published(self, flag: bool = True):
        if self.model and isinstance(self.model, models.Model):
            self.model.is_published = flag
            self.save_model()


class UserWrapper(AbstractWrapper):
    model_class: Type[User] = User

    def __init__(self):
        self.username: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None

        AbstractWrapper.__init__(self, {
            'email': dummy_validator,
            'username': dummy_validator,
            'password': dummy_validator,
        })

    def load_model(self, loaded_model: User) -> 'UserWrapper':
        super().load_model(loaded_model)
        self.username = loaded_model.username
        self.email = loaded_model.email
        self.password = loaded_model.password
        return self

    def retrieve_model(self) -> None:
        self.model = User.objects.get(username=self.username, email=self.email)

    def make_new_model(self) -> None:
        self.model = User.objects.create_user(username=self.username,
                                              email=self.email,
                                              password=self.password)

    def __str__(self):
        return f'<UserWrapper\n' \
               f'email={self.email}\n' \
               f'username={self.username}\n' \
               f'password={self.password}>'

    def __repr__(self):
        return self.__str__()


class CategoryWrapper(PublishedWrapper):
    model_class: Type[Category] = Category

    def __init__(self):
        self.category_name: Optional[str] = None

        PublishedWrapper.__init__(self, {
            'category_name': dummy_validator
        })

    def load_model(self, loaded_model: Category) -> 'CategoryWrapper':
        super().load_model(loaded_model)
        self.category_name = loaded_model.category
        return self

    def retrieve_model(self) -> None:
        self.model: Category = self.model_class.objects.get(category=self.category_name)

    def make_new_model(self) -> None:
        self.model: Category = self.model_class(category=self.category_name, is_published=False)

    def __str__(self):
        return '<CategoryWrapper category_name={}>'.format(self.category_name)

    def __repr__(self):
        return self.__str__()


class TutorialAnchorWrapper(PublishedWrapper):
    model_class: Type[Tutorial] = Tutorial

    def __init__(self):
        self.url: Optional[str] = None
        self.name: Optional[str] = None
        self.categories: Optional[Iterable[CategoryWrapper]] = None

        PublishedWrapper.__init__(self, {
            'url': dummy_validator,
            'name': dummy_validator,
            'categories': dummy_validator,
        })
        SettableBase.__init__(self)

    def load_model(self, loaded_model: Tutorial) -> 'TutorialAnchorWrapper':
        super().load_model(loaded_model)
        self.url = loaded_model.url
        self.name = loaded_model.name
        self.categories = [CategoryWrapper().load_model(cat) for cat in loaded_model.categories.all()]
        return self

    def retrieve_model(self) -> None:
        self.model: Tutorial = self.model_class.objects.get(url=self.url, name=self.name)

    def make_new_model(self) -> None:
        self.model: Tutorial = self.model_class(url=self.url, name=self.name, is_published=False)

    def prepare_model(self) -> None:
        self.finalize_prerequisite_wrapper_iter(self.categories)

    def finalize_model(self) -> None:
        self.save_model()
        self.model.categories.set(wrapper.model for wrapper in self.categories)
        self.save_model()

    def __str__(self):
        return f'<TutorialWrapper\n' \
               f'url={self.url}\n' \
               f'name={self.name}\n' \
               f'categories={self.categories}>'

    def __repr__(self):
        return self.__str__()


class GraphWrapper(PublishedWrapper):
    model_class: Type[Graph] = Graph

    def __init__(self):
        self.url: Optional[str] = None
        self.name: Optional[str] = None
        self.categories: Optional[Iterable[CategoryWrapper]] = None
        self.authors: Optional[Iterable[UserWrapper]] = None
        self.priority: Optional[int] = None
        self.cyjs: Optional[dict] = None
        self.tutorials: Optional[Iterable[TutorialAnchorWrapper]] = None

        PublishedWrapper.__init__(self, {
            'url': dummy_validator,
            'name': dummy_validator,
            'categories': dummy_validator,
            'authors': dummy_validator,
            'priority': dummy_validator,
            'cyjs': dummy_validator,
            'tutorials': dummy_validator
        })

    def load_model(self, loaded_model: Graph) -> 'GraphWrapper':
        super().load_model(loaded_model)
        self.url = loaded_model.url
        self.name = loaded_model.name
        self.categories = [CategoryWrapper().load_model(cat) for cat in loaded_model.categories.all()]
        self.authors = [UserWrapper().load_model(user) for user in loaded_model.authors.all()]
        self.priority = loaded_model.priority
        self.cyjs = loaded_model.cyjs
        self.tutorials = [TutorialAnchorWrapper().load_model(tutorial_anchor)
                          for tutorial_anchor in loaded_model.tutorials.all()]
        return self

    def retrieve_model(self) -> None:
        self.model: Graph = self.model_class.objects.get(url=self.url, name=self.name)

    def make_new_model(self) -> None:
        self.model: Graph = self.model_class(url=self.url, name=self.name,
                                             priority=self.priority, cyjs=self.cyjs,
                                             is_published=False)

    def prepare_model(self) -> None:
        self.finalize_prerequisite_wrapper_iter(self.categories)
        self.finalize_prerequisite_wrapper_iter(self.tutorials)
        self.finalize_prerequisite_wrapper_iter(self.authors)

    def finalize_model(self) -> None:
        self.save_model()

        self.model.categories.set(wrapper.model for wrapper in self.categories)
        self.model.tutorials.set(wrapper.model for wrapper in self.tutorials)
        self.model.authors.set(wrapper.model for wrapper in self.authors)

        self.save_model()

    def __str__(self):
        return f'<GraphWrapper url={self.url} \n' \
               f'name={self.name}\n' \
               f'categories={self.categories}\n' \
               f'authors={self.authors}\n' \
               f'priority={self.priority}\n' \
               f'cyjs={self.cyjs}\n' \
               f'tutorials={self.tutorials}\n' \
               f'>'

    def __repr__(self):
        return self.__str__()


class CodeWrapper(AbstractWrapper):
    model_class: Type[Code] = Code

    def __init__(self):
        self.tutorial: Optional[TutorialAnchorWrapper] = None
        self.code: Optional[str] = None

        AbstractWrapper.__init__(self, {
            'tutorial': dummy_validator,
            'code': dummy_validator
        })

    def retrieve_model(self) -> None:
        self.model: Code = self.model_class(tutorial=self.tutorial.model)

    def make_new_model(self) -> None:
        self.model: Code = self.model_class(tutorial=self.tutorial.model, code=self.code)

    def __str__(self):
        return f'<CodeWrapper\n' \
               f'tutorial={self.tutorial}\n' \
               f'code={self.code}>'

    def __repr__(self):
        return self.__str__()


class ExecResultJsonWrapper(AbstractWrapper):
    model_class: Type[ExecResultJson] = ExecResultJson

    def __init__(self):
        self.code: Optional[CodeWrapper] = None
        self.graph: Optional[GraphWrapper] = None
        self.json: Optional[Mapping] = None

        AbstractWrapper.__init__(self, {
            'code': dummy_validator,
            'graph': dummy_validator,
            'json': dummy_validator,
        })

    def retrieve_model(self) -> None:
        self.model: ExecResultJson = self.model_class.objects.get(code=self.code.model, graph=self.graph.model)

    def make_new_model(self) -> None:
        self.model: ExecResultJson = self.model_class(code=self.code.model, graph=self.graph.model, json=self.json)

    def __str__(self):
        return f'<ExecResultWrapper\n' \
               f'code={self.code}\n' \
               f'graph={self.graph}\n' \
               f'json={self.json}>'

    def __repr__(self):
        return self.__str__()


class TutorialTranslationContentWrapper(PublishedWrapper):
    def __init__(self):
        self.model_class: Optional[Type[TranslationBase]] = None

        self.title: Optional[str] = None
        self.authors: Optional[Iterable[UserWrapper]] = None
        self.tutorial_anchor: Optional[TutorialAnchorWrapper] = None
        self.abstract: Optional[str] = None
        self.content_md: Optional[str] = None
        self.content_html: Optional[str] = None

        PublishedWrapper.__init__(self, {
            'title': dummy_validator,
            'authors': dummy_validator,
            'tutorial_anchor': dummy_validator,
            'abstract': dummy_validator,
            'content_md': dummy_validator,
            'content_html': dummy_validator,
        })

    def set_model_class(self, model_class: Type[TranslationBase]) -> None:
        self.model_class = model_class

    def set_variables(self, **kwargs) -> 'TutorialTranslationContentWrapper':
        super().set_variables(**kwargs)
        the_model_class = kwargs.get('model_class', None)
        if the_model_class and issubclass(the_model_class, TranslationBase):
            self.set_model_class(the_model_class)
        return self

    def retrieve_model(self) -> None:
        self.model: TranslationBase = self.model_class.objects.get(tutorial_anchor=self.tutorial_anchor.model)

    def make_new_model(self) -> None:
        self.model: TranslationBase = self.model_class(title=self.title,
                                                       tutorial_anchor=self.tutorial_anchor.model,
                                                       abstract=self.abstract,
                                                       content_md=self.content_md,
                                                       content_html=self.content_html)

    def prepare_model(self) -> None:
        self.finalize_prerequisite_wrapper_iter(self.authors)

    def finalize_model(self) -> None:
        self.save_model()
        self.model.authors.set(wrapper.model for wrapper in self.authors)
        self.save_model()

    def __str__(self):
        return f'<TutorialContentWrapper\n' \
               f'model_class={self.model_class}\n' \
               f'model={self.model}\n' \
               f'title={self.title}\n'\
               f'tutorial_anchor={self.tutorial_anchor.model}\n'\
               f'abstract={self.abstract}\n'\
               f'content_md={self.content_md}\n'\
               f'content_html={self.content_html}>'

    def __repr__(self):
        return self.__str__()


class GraphTranslationContentWrapper(PublishedWrapper):
    def __init__(self):
        self.model_class: Optional[Type[GraphTranslationBase]] = None

        self.title: Optional[str] = None
        self.abstract: Optional[str] = None
        self.graph_anchor: Optional[GraphWrapper] = None

        PublishedWrapper.__init__(self, {
            'title': dummy_validator,
            'abstract': dummy_validator,
            'graph_anchor': dummy_validator,
        })

    def set_model_class(self, model_class: Type[GraphTranslationBase]) -> None:
        self.model_class = model_class

    def set_variables(self, **kwargs) -> 'GraphTranslationContentWrapper':
        super().set_variables(**kwargs)
        the_model_class = kwargs.get('model_class', None)
        if the_model_class and issubclass(the_model_class, GraphTranslationBase):
            self.set_model_class(the_model_class)
        return self

    def retrieve_model(self) -> None:
        self.model: GraphTranslationBase = self.model_class.objects.get(graph_anchor=self.graph_anchor.model)

    def make_new_model(self) -> None:
        self.model: GraphTranslationBase = self.model_class(graph_anchor=self.graph_anchor,
                                                            title=self.title,
                                                            abstract=self.abstract)

    def __str__(self):
        return f'<GraphContentWrapper\n' \
               f'model_class={self.model_class}\n' \
               f'model={self.model}\n' \
               f'title={self.title}\n' \
               f'abstract={self.abstract}\n' \
               f'graph_anchor={self.graph_anchor}>'

    def __repr__(self):
        return self.__str__()
