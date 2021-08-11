# `Code` Table

The `Code` table describes runnable code snippets. 

## Mixins

* [`UUIDMixin`](/RFCs/backend/database/mixins.md#UUIDMixin)
* [`TimeDateMixin`](/RFCs/backend/database/mixins.md#TimeDateMixin)

## Fields

|       Field       |                             Type                             | Description |
| :---------------: | :----------------------------------------------------------: | :---------: |
|      `name`       |                      `models.TextField`                      |             |
|      `code`       |                      `models.TextField`                      |             |
| `tutorial_anchor` | [`FK(TutorialAnchor)`](/RFCs/backend/database/tutorial_related_tables/tutorial/tutorial_anchor_table.md) |             |

