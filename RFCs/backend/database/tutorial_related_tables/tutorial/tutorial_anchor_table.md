# `TutorialAnchor` Table

A tutorial anchor serves as an entry point to every tutorial, since it contains a unique URL from which users can access the tutorial content. The anchor may contain other useful metadata. 

## Mixins

* [`UUIDMixin`](/RFCs/backend/database/mixins.md#UUIDMixin)
* [`TimeDateMixin`](/RFCs/backend/database/mixins.md#TimeDateMixin)
* [`StatusMixin`](/RFCs/backend/database/mixins.md#StatusMixin)

## Fields 

| Field  |                             Type                             |                         Description                          |
| :----: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| `url`  |                      `models.CharField`                      | The unique URL pointing to the corresponding tutorial content. |
| `name` |                      `models.TextField`                      |               The unique name for this anchor.               |
| `tags` | [`FK(TutorialTag)`](/RFCs/backend/database/tutorial_related_tables/tag/tutorial_tag_table.md) |        The tutorial tags associated with this anchor.        |

