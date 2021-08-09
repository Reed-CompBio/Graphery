# Introduction

This document explains the terms used in the database classes. 

## Tag

|     Term     |             Description              |
| :----------: | :----------------------------------: |
| tutorial tag | The tags that are used by tutorials. |
|  graph tag   |  The tags that are used by graphs.   |

## Tutorial

|                 Term                  |                         Description                          |
| :-----------------------------------: | :----------------------------------------------------------: |
|             tutorial URL              | The URL that users use to access the corresponding tutorial content. |
|            tutorial anchor            | The table that is used to store tutorials' metadata. This includes the `tutorial url`, `tutorial anchor name`, `tutorial tags`, etc.  See `tutorial_anchor_table.md` for more information. |
|         tutorial anchor name          |                The name of a tutorial anchor.                |
|             tutorial tag              |        See `tutorial tag` above in the `Tag` section.        |
|         tutorial translation          | The translation of a tutorial. This includes the `tutorial translation title`, `tutorial translation authors`, `tutorial translation abstract`, etc. Note that English (the default language of this site) is a special case of tutorial content. See `tutorial_translation_table.md` and documents for its subclasses for more information. |
|      tutorial translation title       |             `The title of a tutorial translation             |
|      tutorial translation author      |             The author of a tutorial translation             |
|     tutorial translation abstract     |            The abstract of a tutorial translation            |
|     tutorial translation content      |          The main content of a tutorial translation          |
| tutorial translation content markdown |    The markdown version of a tutorial translation content    |
|   tutorial translation content html   |      The HTML version of a tutorial translation content      |