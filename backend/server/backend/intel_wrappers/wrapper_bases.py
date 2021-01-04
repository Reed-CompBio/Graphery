from __future__ import annotations

from abc import abstractmethod, ABC

from typing import Optional, Iterable, Mapping, Callable, Any, Type, Union, MutableMapping, TypeVar, Generic

from django.core.exceptions import ValidationError
from django.db import models, IntegrityError, transaction
from django.db.models import Model

from backend.intel_wrappers.validators import is_published_validator, dummy_validator
from backend.model.mixins import PublishedMixin, UUIDMixin


class _EmptyValue:
    pass


class IntelWrapperBase(ABC):
    def __init__(self, validators: Mapping[str, Callable]):
        self.validators = validators

    def validate(self):
        for field_name, validator in self.validators.items():
            # TODO change error class
            field = getattr(self, field_name, _EmptyValue)
            if field == _EmptyValue:
                raise AssertionError('Cannot find the field `%s` during validation' % field_name)
            try:
                validator(field)
            except AssertionError as e:
                e.args = f'The field {field_name} does not pass the validator and has following error: {e}',
                raise
            except Exception as e:
                e.args = f'Unknown error occurs during validating field {field_name}. Error: {e}',
                raise


_T = TypeVar('_T', bound=Model)


class ModelWrapperBase(Generic[_T], ABC):
    model_class: Optional[Type[_T]] = None

    def __init__(self):
        self.model: Optional[_T] = None

    def model_exists(self) -> bool:
        return self.model and isinstance(self.model, models.Model)

    @classmethod
    def set_model_class(cls, model_class: Type[_T]) -> None:
        cls.model_class = model_class

    def load_model_var(self, loaded_model: _T) -> None:
        pass

    def load_model(self, loaded_model: _T, load_var: bool = True) -> ModelWrapperBase:
        self.model = loaded_model

        if load_var:
            self.load_model_var(loaded_model)

        return self

    @abstractmethod
    def retrieve_model(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def make_new_model(self) -> None:
        raise NotImplementedError

    def get_model(self, validate: bool = True) -> None:
        if not self.model_class:
            raise AssertionError
        # TODO use other error
        # TODO use get_or_create (write it manually)

    def overwrite_model(self) -> None:
        raise NotImplementedError

    def prepare_model(self) -> None:
        pass

    def _finalize_model_helper(self, overwrite: bool) -> None:
        raise NotImplementedError

    def finalize_model(self) -> None:
        self.save_model()

    def save_model(self) -> None:
        if self.model_exists():
            try:
                self.model.save()
            except IntegrityError as e:
                raise AssertionError('A exception occurs during saving the model {}. Error: {}'
                                     .format(self.model, e))
        else:
            raise AssertionError('Cannot save %s since model does not exist.' % self)

    def delete_model(self) -> _T:
        if self.model_exists():
            return self.model.delete()
        else:
            raise AssertionError('Cannot delete %s since model does not exist.' % self)


class SettableBase(ABC):
    def set_variables(self, **kwargs) -> SettableBase:
        return self

    @staticmethod
    def get_var_from_kwargs(kwargs: Mapping, var_name: str) -> Optional[Any]:
        return kwargs.get(var_name, None)


_S = TypeVar('_S', bound=UUIDMixin)


class AbstractWrapper(IntelWrapperBase, ModelWrapperBase[_S], SettableBase, Generic[_S], ABC):
    def __init__(self, validators: MutableMapping[str, Callable]):
        self.id: Optional[str] = None
        validators['id'] = dummy_validator

        IntelWrapperBase.__init__(self, validators)
        ModelWrapperBase.__init__(self)
        SettableBase.__init__(self)

        self.field_names = [*self.validators.keys()]

    def retrieve_model(self) -> None:
        self.model: _S = self.model_class.objects.get(id=self.id)

    def load_model_var(self, loaded_model: _S) -> None:
        super().load_model_var(loaded_model)
        self.id = loaded_model.id

    def set_variables(self, **kwargs) -> AbstractWrapper[_S]:
        for key, value in kwargs.items():
            if key in self.field_names:
                setattr(self, key, value)
            else:
                raise ValueError(f'The field name {key} is not in specified fields {self.field_names}')
                # TODO

        return self

    def overwrite_model(self) -> None:
        if not self.model_exists():
            return

        for field in self.validators.keys():
            # directly setting values will cause problems since in many to many / many to one fields
            # I can only use model.add/set methods to overwrite values
            # When the field is a many to many field or a generated many to many field or a many to one field
            # the field type in Django ORM is a subclass class of Manager, generated by
            # create_forward_many_to_many_manager(), create_reverse_many_to_one_manager()
            # in related_descriptors.py
            field_value: Union[Iterable[ModelWrapperBase], ModelWrapperBase, Any] = getattr(self, field)
            models_field = getattr(self.model, field)

            if isinstance(models_field, models.Manager):
                if not (isinstance(field_value, Iterable) and
                        all(isinstance(field_wrapper, ModelWrapperBase) for field_wrapper in field_value)):
                    raise ValueError('Many-to-many/many-to-one field only accepts iterable wrapper collections')
                models_field.set(model_wrapper.model for model_wrapper in field_value)
            else:
                if isinstance(field_value, ModelWrapperBase):
                    setattr(self.model, field, field_value.model)
                else:
                    setattr(self.model, field, field_value)

    def get_model(self, validate: bool = True) -> bool:
        if validate:
            try:
                self.validate()
                super().get_model()
            except AssertionError as e:
                e.args = 'Something went wrong when validating variables {} for the model {}. Error: {}' \
                             .format(list(self.validators.keys()), self.model_class, e),
                raise

        try:
            self.retrieve_model()
            return False
        except (self.model_class.DoesNotExist, ValidationError):
            if validate:
                self.make_new_model()
                self.id = self.model.id
                return True
            else:
                raise AssertionError('Cannot make new model without validations!')
        except self.model_class.MultipleObjectsReturned as e:
            # which should never happen
            raise AssertionError('Multiple model instances received with model {} and variables {}. Error: {}'
                                 .format(self.model_class, list(self.validators.keys()), e))

    def _finalize_model_helper(self, overwrite: bool) -> None:
        if overwrite:
            self.validate()
            self.overwrite_model()

    def finalize_model(self, overwrite: bool = True, validate: bool = True) -> None:
        with transaction.atomic():
            self.prepare_model()
            is_newly_created = self.get_model(validate=validate)
            if is_newly_created:
                if not overwrite or not validate:
                    raise AssertionError('When a model is created, the overwrite flag and validate flag must be True.')
                self.save_model()
            self._finalize_model_helper(overwrite=overwrite)
            if overwrite and validate:
                self.save_model()


_V = TypeVar('_V', bound=PublishedMixin)


class PublishedWrapper(AbstractWrapper[_V], Generic[_V], ABC):
    def __init__(self, validators: MutableMapping[str, Callable]):
        self.is_published: bool = False
        validators['is_published'] = is_published_validator
        super(PublishedWrapper, self).__init__(validators)

    def load_model_var(self, loaded_model: _V) -> None:
        super().load_model_var(loaded_model)
        self.is_published = loaded_model.is_published


class VariedContentWrapper(PublishedWrapper[_V], Generic[_V], ABC):
    def __init__(self, validators: MutableMapping[str, Callable]):
        super(VariedContentWrapper, self).__init__(validators)

        self.model_class: _V = self.model_class
