# `TutorialAnchor` Table

A tutorial anchor serves as an entry point to every tutorial, since it contains a unique URL from which users can access the tutorial content. The anchor may contain other useful metadata. 

## Mixins

* [`UUIDMixin`](/RFCs/backend/database/mixins.md#UUIDMixin)
* `TimeDateMixin`
* `StatusMixin`

## Fields 

| Field  |        Type        | Description |
| :----: | :----------------: | :---------: |
| `url`  | `models.CharField` |             |
| `name` | `models.TextField` |             |
| `tags` | `FK(TutorialTag)`  |             |

