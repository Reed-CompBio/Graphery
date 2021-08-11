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
|               tutorial                | A tutorial, consisting of four parts: textual content, graphs, code, and code execution result. |
|           textual tutorial            |         Also know as the text content of a tutorial          |
|              tutorial ID              |               The unique UUID of the tutorial.               |
|             tutorial URL              | The URL that users use to access the corresponding tutorial content. |
|            tutorial anchor            | a collection of a tutorial's metadata. This includes the `tutorial url`, `tutorial anchor name`, `tutorial tags`, etc.  See `tutorial_anchor_table.md` for more information. |
|         tutorial anchor name          |                The name of a tutorial anchor.                |
|             tutorial tag              |        See `tutorial tag` above in the `Tag` section.        |
|         tutorial translation          | The translation of a tutorial. This includes the `tutorial translation title`, `tutorial translation authors`, `tutorial translation abstract`, etc. Note that English (the default language of this site) is a special case of tutorial content. See `tutorial_translation_table.md` and documents for its subclasses for more information. |
|      tutorial translation title       |             `The title of a tutorial translation             |
|      tutorial translation author      |             The author of a tutorial translation             |
|     tutorial translation abstract     |            The abstract of a tutorial translation            |
|     tutorial translation content      |          The main content of a tutorial translation          |
| tutorial translation content markdown |    The markdown version of a tutorial translation content    |
|   tutorial translation content html   |      The HTML version of a tutorial translation content      |

## Graph

|             Term             |                         Description                          |
| :--------------------------: | :----------------------------------------------------------: |
|         graph anchor         |              a collection of a graph's metadata              |
|           graph ID           |                The unique UUID of the graph.                 |
|          graph URL           |  The URL that users use to access the corresponding graph.   |
|          graph name          |                    The name of the graph.                    |
|          graph JSON          | The JSON description of the an actual graph. The format is in CYJS. |
|          graph tag           |               Tag associated with this graph.                |
|         graph maker          |                   Maker of the graph JSON.                   |
|         graph source         |                   The source of the graph.                   |
|        graph content         | The descrition of graphs in JSON and other format. This is different than the graph description. See below for more details. |
|      graph description       | The table storing textual descriptionsof a graph, which states what the graph is about, etc. |
|   graph description title    |              The title of the graph description              |
|  graph description content   |              The textual description of a graph              |
| tutorial of this graph (TBD) |            The tutorial that's using this graph.             |

## Code

|         Term         |                  Description                   |
| :------------------: | :--------------------------------------------: |
|       code ID        |          The unique UUID of the code           |
|     code content     |             The actual texual code             |
| tutorial of the code | The unique tutorial that talks about the code. |

## Execution Result

|        Term         |                   Description                    |
| :-----------------: | :----------------------------------------------: |
| Execution Result ID |      The unique UUID of a execution result.      |
|  Execution Result   | The execution result of some code on some graph. |

## Uploads

|       Term       |                         Description                         |
| :--------------: | :---------------------------------------------------------: |
|    upload URL    |      The unique URL pointing to the uploaded resource.      |
|    upload ID     |          The unique UUID of the uploaded resource.          |
| uploaded content | The content that's uploaded as an attachment to the server. |

