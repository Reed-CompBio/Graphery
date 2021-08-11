# `GraphContent` Table

The `GraphContent` table stores abstract descriptions of graphs in JSON and other format, if applicable. This is different than the textual description of graphs. See the [term explanation](/RFCs/backend/database/tutorial_related_tables/introduction.md#Graph) for more details.  

## Mixins 

* [`UUIDMixin`](/RFCs/backend/database/mixins.md#UUIDMixin)
* [`TimeDateMixin`](/RFCs/backend/database/mixins.md#TimeDateMixin)
* [`StatusMixin`](/RFCs/backend/database/mixins.md#StatusMixin) (Note: the `_default_status` is set to `PUBLISHED`)

## Fields

|     Field      |                             Type                             |             Desciption              |
| :------------: | :----------------------------------------------------------: | :---------------------------------: |
| `graph_anchor` | [`OTO(GraphAnchor)`](/RFCs/backend/database/tutorial_related_tables/graph/graph_anchor_table.md) | The graph meta data of this graph.  |
|    `makers`    | [`MTM(User)`](/RFCs/backend/database/user_system/user_table.md) |      The makers of this graph       |
|     `cyjs`     |                      `models.JSONField`                      | graph description in `cyjs` format. |