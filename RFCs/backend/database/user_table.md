# User Table 

The user table inherits [`UUIDMixin`](./mixins.md#UUIDMixin) and [`User`](https://docs.djangoproject.com/en/3.2/ref/contrib/auth/) model. View the link to see more properties of the `User` model. The inherited model extends `User` with new properties `role` and `is_verified`. 

|       Field        |                             Type                             |                         Description                          |
| :----------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|       `role`       | [`PositiveSmallIntegerField` with `choices` option](https://docs.djangoproject.com/en/3.2/ref/models/fields/#positivesmallintegerfield) | The `role` field indicates the privilege this user has. Currently, there are 6 levels (two level more than the first version of Graphery). Listed from high to low are `Administrator`, `Editor`, `Author`, `Translator`, `Visitor`, and `Reader`. Detailed descriptions of each row are listed in the table down below. |
|   `is_verified`    | [`BooleanField`](https://docs.djangoproject.com/en/3.2/ref/models/fields/#booleanfield) | `is_verified` is used to indicate whether the user has validated their email or not. Unverified users can't perform certain actions. Detailed descriptions are also listed down below. Also, the unverified users are active within <a id="UNVERIFIED_USER_REMOVE_AFTER">`$UNVERIFIED_USER_REMOVE_AFTER` </a>days after the registration. |
| `has_email_update` | [`BooleanField`](https://docs.djangoproject.com/en/3.2/ref/models/fields/#booleanfield) | `has_email_update` is used to indicate whether the user has opted in emails updates when new tutorials are published or when some news is shared by the administrators. |

|     `role`      |                         Description                          | Restriction If Unverified |
| :-------------: | :----------------------------------------------------------: | ------------------------- |
| `Administrator` | `Administrator`s have all the privileges: `view`, `add`, `edit`, `delete` tutorials and other contents, `view`,  `add`, `change`, `delete` users and have access to the Django admin site. |                           |
|    `Editor`     | `Editor`s have access to `view`,  `add`, `edit`, `delete` privileges for tutorials and other contents. |                           |
|    `Author`     | `Author`s have access to `view`, `add`, `edit` privileges for tutorials and other contents. |                           |
|  `Translator`   | `Translators` have access to `view` and `edit` privileges for tutorials but only `view` privileges for other contents. |                           |
|    `Visitor`    | `Visitors` can only `view` the tutorials and other content in the control panel. |                           |
|    `Reader`     |                    No special privileges.                    |                           |

The overwritten `User` model requires a matching [`UserManager`](https://github.com/django/django/blob/main/django/contrib/auth/models.py#L129). It should overwrite [`create_user`](https://github.com/django/django/blob/854e9b066850b9b4eb1171966e996322b2c16d27/django/contrib/auth/models.py#L149) and [`create_superuser`](https://github.com/django/django/blob/main/django/contrib/auth/models.py#L154) functions. Developers should create `User` object only through the helper functions. 
