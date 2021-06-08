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

The subfolder, topic folder, in each category folder should concern one and only topic. The name of each directory should be in English and in lower case. There should not be any loose documents aside from `introduction.md` in each category folder, that is, every document except `introduction.md` in a category folder should be contained in a topic folder. For example, 

<!-- 
# RFCs
## backend 
### introduction.md
### env list.md
### database specification
#### guidelines.md
#### tutorial table.md
#### member table.md
#### ...
### api specification
#### guidelines.md 
#### python seeker api.md
#### ...
## frontend
### env list.md
### introduction.md
### ui design
#### ...
### data/storage structure design
#### ...
### introduction.md
## tutorials
### introduction.md
### for writers
#### ...
### for editors
#### ... 
-->

```text
.
└── RFCs
    ├── backend
    │   ├── introduction.md
    │   ├── env list.md
    │   ├── database specification
    │   │   ├── guidelines.md
    │   │   ├── tutorial table.md
    │   │   ├── member table.md
    │   │   └── ...
    │   └── api specification
    │       ├── guidelines.md
    │       ├── python seeker api.md
    │       └── ...
    ├── frontend
    │   ├── env list.md
    │   ├── introduction.md
    │   ├── ui design
    │   │   └── ...
    │   ├── data/storage structure design
    │   │   └── ...
    │   └── introduction.md
    └── tutorials
        ├── introduction.md
        ├── for writers
        │   └── ...
        └── for editors
            └── ...
```

Each topic folder may have subfolders. The subfolders should be used to compartmentalize the documents in the topic folder. The structure of the subfolders depends on the author of the topic folder. 

## Document Naming Convention

The name of each document should be in English and  in lower case. The names should be the clear, concise and impart the subject of that document. For example, the name of a document about websocket API can be `websocket api.md`. 

## Document Writing

Every document must be in `markdown` format and have one and only one H1 header which should be the same as the document file name except the restriction on caps. For example, the file name of this document is `guidelines.md`, so the H1 header is `Guidelines`. 

Every document should concern one and only one topic. The subheaders should be in order. That is, a H3 header cannot be created without a H2 header as its parent. 

There are no restrictions on the internal structure of each document. 

There can be some places where authors would like to define some environment variables so that the values can be customized later. In this case, the environment variable should be indicated by a string enclosed in a code block (i.e. ``) which starts with a dollar sign ($) and the name of the variable matching the naming convention for constant variables. For example, a user should be removed if they have been unverified for some amount of time after the registration. The amount of time can be a environment variable `$UNVERIFIED_USER_REMOVE_AFTER`. All the environment variables should be compiled into the `env list.md` file in the corresponding category folder by the creator. 

## Committing and Pushing

Each commit should only concern one topic. Do not commit multiple files residing in different topic folders. All the RFCs should be pushed to `RFCs-dev` branch. They must be reviewed before being PRed to `RFCs` branch. 
