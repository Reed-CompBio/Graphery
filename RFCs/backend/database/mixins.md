# Mixins 

This document introduces some of the mixins used by the models in Graphery. All mixins are subclasses of [`models.Model`](https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model) with the [`abstract` property](https://docs.djangoproject.com/en/3.2/topics/db/models/#abstract-base-classes) in its [`Meta` class](https://docs.djangoproject.com/en/3.2/ref/models/options/) set to `True`. For example, 

```python
from django.db import models

class PersonMixin(models.Model):
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        abstract = True
```

## UUIDMixin

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



## TimeDateMixin

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

## PublishedMixin

