# `Uploads` Table

The `Uploads` table contains all the upload file used in the textual tutorial content. 

## Mixins

* [`UUIDMixin`](/RFCs/backend/database/mixins.md#UUIDMixin)
* [`TimeDateMixin`](/RFCs/backend/database/mixins.md#TimeDateMixin)

## Fields

|    Fields     |         Type         | Description |
| :-----------: | :------------------: | :---------: |
|    `file`     |  `models.FileField`  |             |
|    `alias`    |  `models.TextField`  |             |
| `to_tutorial` | `FK(TutorialAnchor)` |             |
|  `to_graph`   |  `FK(GraphAnchor)`   |             |

