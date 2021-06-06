# Guidelines

## Directory Structure 

The `RFCs` folder should be the root folder for all RFCs. No other folders should be create on the same level as the `RFCs` folder. 

There are currently three category folders under the root folder: `backend`, `frontend`, `tutorials`. The `backend` folder contains the RFCs that are related to the backend. Similarly, the RFCs for the frontend goes into the `frontend` folder. The `tutorials` folder contains the guidelines for the writers and editors of the tutorials. 

The subfolder, topic folder, in each category folder should concern one and only topic. There should not be any loose documents aside from `introduction.md` in each category folder, that is, every document except `introduction.md` in a category folder should be contained in a topic folder. 

Each topic folder may have subfolders. The subfolders should be used to compartmentalize the documents in the topic folder. The structure of the subfolders depends on the author of the topic folder. 

## Document Naming Convention

The name of each document should be in lower case. The name of each document should be the clear, concise and impart the subject of that document. 

## Document Writing

Every document must have a H1 header which should be the same name as the document file name. Every document should concern one and only one topic. The subheaders should be in order. That is, a H3 header cannot be created without a H2 header as its parent. 

There are no restrictions on the internal structure of each document. 

## Committing and Pushing

Each commit should only concern one topic. Do not commit multiple files residing in different topic folders. All the RFCs should be pushed to `RFCs-dev` branch. They must be reviewed before being PRed to `RFCs` branch. 
