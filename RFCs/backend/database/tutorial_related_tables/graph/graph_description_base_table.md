# `GraphDescriptionBase` Table

The `GraphDescriptionBase` table is similar to [`TutorialTranslationBase`](/RFCs/backend/database/tutorial_related_tables/tutorial/tutorial_translation_base_table.md) and contains entries that describe what each graph is about. 

## Mixins

* [`UUIDMixin`](/RFCs/backend/database/mixins.md#UUIDMixin)
* [`TimeDateMixin`](/RFCs/backend/database/mixins.md#TimeDateMixin)
* [`StatusMixin`](/RFCs/backend/database/mixins.md#StatusMixin)

## Fields

|      Fields       |                             Type                             | Description |
| :---------------: | :----------------------------------------------------------: | :---------: |
| `tutorial_anchor` | [`OTO(GraphAnchor)`](/RFCs/backend/database/tutorial_related_tables/graph/graph_anchor_table.md) |             |
|     `authors`     | [`MTM(User)`](/RFCs/backend/database/user_system/user_table.md) |             |
|      `title`      |                      `models.TextField`                      |             |
|   `description`   |                      `models.TextField`                      |             |

