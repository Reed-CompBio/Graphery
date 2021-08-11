# `GraphAnchor` Table

The `GraphAnchor` is used to store all the graphs' metadata. This class is very similar to [ `TutorialAnchor`](/RFCs/backend/database/tutorial_related_tables/tutorial/tutorial_anchor_table.md) class. 

## Mixins

* [`UUIDMixin`](/RFCs/backend/database/mixins.md#UUIDMixin)
* [`TimeDateMixin`](/RFCs/backend/database/mixins.md#TimeDateMixin)
* [`StatusMixin`](/RFCs/backend/database/mixins.md#StatusMixin)

## Fields

| Field    | Type                                                         | Description                                         |
| -------- | ------------------------------------------------------------ | --------------------------------------------------- |
| `url`    | `models.CharField`                                           | The unique URL pointing to the corresponding graph. |
| `name`   | `models.TextField`                                           | The unique name for this anchor.                    |
| `tags`   | [`FK(TutorialTag)`](/RFCs/backend/database/tutorial_related_tables/tag/tutorial_tag_table.md) | The graph tags associated with this anchor.         |
| `makers` | [`MTM(User)`](/RFCs/backend/database/user_system/user_table.md) | The makers of this graph                            |

