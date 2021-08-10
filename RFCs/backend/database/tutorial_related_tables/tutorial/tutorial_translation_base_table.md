# `TutorialTranslationBase` Table

Every entry in `TutorialTranslationBase` is linked to one anchor and is the one that's actually holding the textual tutorial . The basic structure of the text content contains a title, paragraphs of actual text in markdown version and html version, an abstract of the main text. It also contains metadata like the authors of the text. 

## Mixins

* [`UUIDMixin`](/RFCs/backend/database/mixins.md#UUIDMixin)
* [`TimeDateMixin`](/RFCs/backend/database/mixins.md#TimeDateMixin)
* [`StatusMixin`](/RFCs/backend/database/mixins.md#StatusMixin)

## Fields

|       Field       |                             Type                             | Description |
| :---------------: | :----------------------------------------------------------: | :---------: |
| `tutorial_anchor` | [`OTO(TutorialAnchor)`](/RFCs/backend/database/tutorial_related_tables/tutorial/tutorial_anchor_table.md) |             |
|     `authors`     | [`MTM(User)`](/RFCs/backend/database/user_system/user_table.md) |             |
|      `title`      |                      `models.TextField`                      |             |
|    `abstract`     |                       models.TextField                       |             |
|   `content_md`    |                       models.TextField                       |             |
|  `content_html`   |                       models.TextField                       |             |

