# `TagBase` Table

`TagBase` is an _abstract_ model where all sets of tags must inherit. It inherites `UUIDMixin` and `PublishedMixin` so that the primary key of every tag is a UUID. It also has a `content` field. 

|     Field     |        Type        |                Description                |
| :-----------: | :----------------: | :---------------------------------------: |
|    `name`     | `models.CharField` | The name of the tag, shown to the public. |
| `description` | `models.TextField` |       The description of this tag.        |

