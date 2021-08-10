# `TutorialTranslation<lang>` Table

`TutorialTranslation<Lang>` inherits the[ `TutorialTranslationBase`](/RFCs/backend/database/tutorial_related_tables/tutorial/tutorial_translation_base_table.md) Table. The `<Lang>` must be replaced with actual language code that's specified in the [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) specification and all language codes must be capital letters. For example, the English translation table must be `TutorialTranslationEN`. 

## Mixins

* [`UUIDMixin`](/RFCs/backend/database/mixins.md#UUIDMixin)
* [`TimeDateMixin`](/RFCs/backend/database/mixins.md#TimeDateMixin)
* [`StatusMixin`](/RFCs/backend/database/mixins.md#StatusMixin)

## Fields

No additional fields. 