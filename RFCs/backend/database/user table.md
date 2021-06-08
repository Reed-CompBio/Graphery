# User Table 

The user table inherits [`User`](https://docs.djangoproject.com/en/3.2/ref/contrib/auth/) model. View the link to see more properties of the `User` model. The inherited model extends `User` with new properties `role` and `is_verified`. 

|     Field     |                         Description                          |
| :-----------: | :----------------------------------------------------------: |
|    `role`     | The `role` field indicates the privilege this user has. Currently, there are 6 levels (two level more than the first version of Graphery). Listed from high to low are `Administrator`, `Editor`, `Author`, `Translator`, `Visitor`, and `Reader`. Detailed descriptions of each row are listed in the table down below. |
| `is_verified` | `is_verified` is used to indicate whether the user has validated their email or not. Unverified users can't perform certain actions. Detailed descriptions are also listed down beblow. Also, the unverified users are active within <a name="UNVERIFIED_USER_REMOVE_AFTER">`$UNVERIFIED_USER_REMOVE_AFTER` </a>days after the registration. |

