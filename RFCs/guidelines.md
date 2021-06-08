# Guidelines

## Directory Structure 

The `RFCs` folder should be the root folder for all RFCs. No other folders should be create on the same level as the `RFCs` folder. That is, the following structure is not acceptable. 

<!-- 
# RFCs
## ...
# something else 
## ... 
-->

```text
.
├── RFCs
│   └── ...
└── something else
    └── ...
```

There are currently three category folders under the root folder: `backend`, `frontend`, `tutorials`. The `backend` folder contains the RFCs that are related to the backend. Similarly, the RFCs for the frontend goes into the `frontend` folder. The `tutorials` folder contains the guidelines for the writers and editors of the tutorials. 

The subfolder, topic folder, in each category folder should concern one and only topic. The name of each directory should follower the naming convention for variables in Python, which means the name should be in lower case and each word is separated by `_`. There should not be any loose documents aside from `introduction.md` and `env_list.md` in each category folder, that is, every document except `introduction.md` and `env_list.md` in a category folder should be contained in a topic folder. For example, 

<!-- 
# RFCs
## backend 
### introduction.md
### env_list.md
### database_specification
#### guidelines.md
#### tutorial_table.md
#### member_table.md
#### ...
### api_specification
#### guidelines.md 
#### python_seeker_api.md
#### ...
## frontend
### env_list.md
### introduction.md
### ui_design
#### ...
### data_storage_structure_design
#### ...
### introduction.md
## tutorials
### introduction.md
### for_writers
#### ...
### for_editors
#### ... 
-->

```text
.
└── RFCs
    ├── backend
    │   ├── introduction.md
    │   ├── env_list.md
    │   ├── database_specification
    │   │   ├── guidelines.md
    │   │   ├── tutorial_table.md
    │   │   ├── member_table.md
    │   │   └── ...
    │   └── api_specification
    │       ├── guidelines.md
    │       ├── python_seeker_api.md
    │       └── ...
    ├── frontend
    │   ├── env_list.md
    │   ├── introduction.md
    │   ├── ui_design
    │   │   └── ...
    │   ├── data_storage_structure_design
    │   │   └── ...
    │   └── introduction.md
    └── tutorials
        ├── introduction.md
        ├── for_writers
        │   └── ...
        └── for_editors
            └── ...
```

Each topic folder may have subfolders. The subfolders should be used to compartmentalize the documents in the topic folder. The structure of the subfolders depends on the author of the topic folder. 

## Document Naming Convention

The name of each document should also follow the naming convention for variables in Python. That is, the name should be in lower case and each word is separated by `_`. The names should be the clear, concise and impart the subject of that document. For example, the name of a document about websocket API can be `websocket_api.md`. 

## Document Writing

Every document must be in `markdown` format and have one and only one H1 header which should be the same as the document file name except it should be in plain English. For example, the file name of this document is `user_table.md`, so the H1 header is `User Table`. 

Every document should concern one and only one topic. The subheaders should be in order. That is, a H3 header cannot be created without a H2 header as its parent. 

There are no restrictions on the internal structure of each document. 

There can be some places where authors would like to define some environment variables so that the values can be customized later. In this case, the environment variable should be indicated by a string enclosed in a code block (i.e. ``) which starts with a dollar sign ($) and the name of the variable matching the naming convention for constant variables. For example, a user should be removed if they have been unverified for some amount of time after the registration. The amount of time can be a environment variable `$UNVERIFIED_USER_REMOVE_AFTER`. All the environment variables should be compiled into the `env_list.md` file in the corresponding category folder by the creator. 

## Committing and Pushing

Each commit should only concern one topic. Do not commit multiple files residing in different topic folders. All the RFCs should be pushed to `RFCs-dev` branch. They must be reviewed before being PRed to `RFCs` branch. 
