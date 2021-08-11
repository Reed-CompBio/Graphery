# Mixins 

This document introduces some of the mixins used by the models in Graphery. All mixins are subclasses of [`models.Model`](https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model) with the [`abstract` property](https://docs.djangoproject.com/en/3.2/topics/db/models/#abstract-base-classes) in its [`Meta` class](https://docs.djangoproject.com/en/3.2/ref/models/options/) set to `True`. For example, 

```python
from django.db import models

class PersonMixin(models.Model):
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        abstract = True
```

## `UUIDMixin`

The `UUIDMixin` overrides the original primary key `id` so that it's a [`models.UUIDField`](https://docs.djangoproject.com/en/3.2/ref/models/fields/#uuidfield). 

| Field |                             Type                             |              Description               |
| :---: | :----------------------------------------------------------: | :------------------------------------: |
| `id`  | [`models.UUIDField`](https://docs.djangoproject.com/en/3.2/ref/models/fields/#uuidfield) | Overrides the type of the primary key |

**Every** model in Graphery must inherit this mixin. That is, every model in Graphery must use UUID as it's primary key. 

```python
from uuid import uuid4
from django.db import models

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True
```



## `TimeDateMixin`

The `TimeDateMixin` is used to record the created time and modified time of entries in models inheriting this mixin. It has two fields: 

|      Field      |                             Type                             |                         Description                          |
| :-------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| `created_time`  | [`models.DateTimeField` with `auto_now_add` option set to `True` or `default` option set to `timezone.now`](https://docs.djangoproject.com/en/3.2/ref/models/fields/#datetimefield) | This records the time of the corresponding entry from some model, when the entry is created. |
| `modified_time` | [`models.DateTimeField` with `auto_now` option set to `True`](https://docs.djangoproject.com/en/3.2/ref/models/fields/#datetimefield) | This records the time of the corresponding entry from some model, when the entry is modified. |

```python
class TimeDateMixin(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

## `PublicManager`

Additionally, this mixin has it's `objects` [manager](https://docs.djangoproject.com/en/3.2/topics/db/managers/#managers) overridden. Details will be posted later. Here are some tools developers might need to create a manager: 

* [`F()` expression](https://docs.djangoproject.com/en/3.2/ref/models/expressions/#f-expressions)
* [`annotate(args*, **kwargs)`](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#annotate)
* [related post](https://stackoverflow.com/a/36996962)

```python
class PublicManager(models.Manager):
    """details coming later"""
    def __init__(self, *args, **kwargs) -> None:
      
    
    def get_public_objects(self) -> QuerySet:
			"""details coming later"""
      pass
```

## `PublishedMixin` (Deprecated)

`PublishedMixin` is used to indicate whether an entry is publicly viewable without privileges. It has a `is_published` boolean field as the indicator. Additionally, a computed property `is_public` is provided to developers so that they use other conditions to determine whether an entry can be seen without privileges. `is_public should be used, instead of `is_published`. 

|     Field      |                             Type                             |                     Description                     |
| :------------: | :----------------------------------------------------------: | :-------------------------------------------------: |
| `is_published` | [`models.BooleanField` with `default` set to `False`](https://docs.djangoproject.com/en/3.2/ref/models/fields/#booleanfield) | This indicates whether an entry is published or not. |

```python
from django.db import models

class PublishedManager(PublicManager):
  def get_public_objects(self) -> QuerySet:
    return self.annotate()

class PublishedMixin(models.Model):
    is_published = models.BooleanField(default=False)

    @property
    def is_public(self) -> bool:
        return self.is_published

    class Meta:
        abstract = True
```

## `StatusMixin`

`StatusMixin` is intended to be a replacement for `PublishedMixin`. In the status mixin, developers can assign statuses other than `published` and `not published`, enabling for more flexible access control. 

|     Field     |        Type        |                         Description                          |
| :-----------: | :----------------: | :----------------------------------------------------------: |
| `item_status` | `models.CharField` | This field, having a size of 20 chars, indicates the status of an item in the database. The content of the `CharIField` is restricted to the following status list. |

### Status List

The status list shows all the possible status code `item_status` can have. All the codes are all caps. 

| Status Name | Status Code | Description                                                  |
| :---------: | :---------: | ------------------------------------------------------------ |
|    draft    |   `DRAFT`   | incomplete and only viewable by anyone with proper user role. |
|  published  | `PUBLISHED` | complete and viewable by everyone.                           |
|  reviewing  | `REVIEWING` | waiting to be published by user with publishing capability.  |
|   private   |  `PRIVATE`  | only viewable by internal staff.                             |
|    trash    |   `TRASH`   | trashed.                                                     |

## Additional Argument 

| Variable Name     | Type  | Description                                              |
| ----------------- | ----- | -------------------------------------------------------- |
| `_default_status` | `str` | The default status used when no status code is supplied. |

