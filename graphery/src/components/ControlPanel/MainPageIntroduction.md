## How to Upload Tutorial 

A tutorial has three parts: text content, graph, and code. However, first you need to creat an anchor. By creating an anchor, you are specifying the URL which users can use to access the tutorial. 


### Create Anchor 

To create an anchor, click on the `Tutorial Anchors` on the left vertical menu. Then, you should be able to see a table displaying existing tutorial anchors, if there is any. To creat a new anchor, click on the `ADD NEW` on top of the table, which should open up a new page. 

In that page, you can see that the ID is pending, which means nothing is created in the database now. Then you need to fill in the `tutorial URL`, `tutorial Name`, and `rank`, as well as categories if you want to. 

Tutorial Name is the name of the tutorial, which just serves as a human-readable string in the database query. However, the name should be informed. We recommend you use the English title of the tutorial as the name. 

The tutorial URL should be informed, that is, users can know what's the tutorial is linked to this url by just looking at the URL. We recommend that you use the tutorial name with characters other than letters and numbers replaced by `-`. 

The rank is a set of number that specifies how tutorials should be order. It's in form of `xxx-x`. Choose the suitable one. The first digit represents the difficulty of the course. And the second two digits is the index of the tutorial within that rank. Since there can be tutorials discussing the same topic, the first three digits should be the same with the digit after the dash, `-`, representing the order of tutorials in the same topic. 

Then you can choose the categories if you like and set if publish status. After clicking the submit button and see a green popup, you are good to go. 


### Upload Tutorial Text Content 

After creating an anchor, you can upload the three parts of the tutorial. 

To upload the tutorial text content, click on `Tutorial Content` and it should bring you to a similar page with a list of stored tutorial text content. To change the language, click on the dropdown manual on the top of the list and chose the language you want. 

If the tutorial has uploaded content, you can click on the title to edit the existing tutorial. If not, the `Title` column will show `<None>` and you can click that to creat add new content.

When you are in the editor page, you can just fill in the content and hit submit to write to the database. Please note that the title is different from the name of the anchor. The title is what users will see on actual tutorial text whereas the name of the anchor is a piece human-readable text for internal use.

Sometime you may need to upload picture. In this case, please go to the `Uploads` tab on the left vertical menu, and hit `ADD NEW`. You can choose the file you want to upload in a proceeding popup.  

### Upload Graph 

Currently, if you have a good graph, please contact the administrator. You can use the existing graphs in the tutorial. 

### Upload Graph Content

The graph content has a similar structure as the tutorial content. 

### Upload Code 

A tutorial should have a code working snippet. To upload a new code snippet, please go the Code tab in the left vertical menu. And click `ADD NEW` on the top of the list table. Simply paste your code in the editor and hit submit. You should wait for a moment since the code is not only being pushing to the database, it's also being run on the associated graphs to generate result JSON. There will be two green popup show if everything goes well. One indicates that the code is uploaded successfully, and the other one indicates that the result JSON is fetched again. At this point, you should check if all the graphs have proper results by going down to the card on the bottom, on which there is a drop down menu you can click to see the execution result for each graph.  


