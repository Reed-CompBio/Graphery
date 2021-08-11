# `ExecutionResult` Table

The `ExecutionResult` table contains the execution results. Each of the result is specified by a code snippet and a graph. 

## Mixins

* [`UUIDMixin`](/RFCs/backend/database/mixins.md#UUIDMixin)
* [`TimeDateMixin`](/RFCs/backend/database/mixins.md#TimeDateMixin)

## Fields

| Field              | Type               | Description |
| ------------------ | ------------------ | ----------- |
| `code`             | `FK(Code)`         |             |
| `graph`            | `FK(GraphAnchor)`  |             |
| `result_json`      | `models.JSONField` |             |
| `result_json_meta` | `models.JSONField` |             |

## Result JSON API

## Result JSON Meta API