# Get Started For Writers

## Introduction 

This is a guide for people who want to contribute tutorials. 

## Components 

A tutorial consists of the following components: categories, a tutorial anchor, tutorial content in different languages, a graph anchor, graph info in different languages, code content, and execution results. 

## Add, Delete, and Modify

Every component can be created in the control panel. Simply by directing to the component page and clicking on `Add New` button, the app will take you to a empty page where you can fill in content and save it to the cloud. 

To delete an entry, click on the red dustbin button at the end of the table, confirm that you know what you are doing the a popup, and the entry should be removed from the database. All deletion is NOT reversible for now. So please be cautious about the delete buttons. Deleting uploads is an exception. You need to click on the upload you want to delete. And you can find the a `Delete PERMANENTLY` button on a popup. Deleting tutorial anchors and graphs is another exception, which will be described in the following sections. 

To modify an existing entry, click on the fist cell corresponding to the entry you want to delete, the app will take you to an editing page. 

Changes are saved only by clicking on the `Submit` buttons. A green popup will follow every successful save. If you don't see one, there is a chance the content is not saved. Please save the content locally on your computer and contact me if you encounter this situation. 

Every unsaved changes will be discarded when you leave the page. There will be a confirm popup so don't worry about hitting go back button by accident. 

# About the structure of the control panel 

Every thing on the control panel table is NOT editable. You have use corresponding editor page to edit content. 

# Some general properties 

`Publish?` Almost every component has this property. If `Publish?` is false, ie. the checkbox is not checked, the content is only visible by writers and administrators. 

`url` Every url must be unique. It only accepts letters, numbers, `-`, and `_`. 

`name` Every name must be unique. It only accepts letters, numbers, space, `-` and `_`.

## Category

The names of the categories are unique. 

## Tutorial Anchor

The tutorial anchor is a weird concept. Every anchor stores the url and the name of a tutorial. It's linked with content in different languages. So, when you want to create a brand new tutorial, that is, not a translation of an existing tutorial, you have to create an anchor first. The name of this anchor should be english name of the tutorial. And the url should be the name except every space is replaced by `-`. 

You can't delete an anchor when there are content associated with it. You have to delete all the content manually first before deleting the anchor. 

## Tutorial Content

In tutorial content page, on the top of the table, a language selector is present. You can use that to navigate to a specific language and the table will load up the tutorial content in that language. The default is loaded to the current language of the user interface. If the tutorial content is not added to the database, a `<None>` label is presented. 

By clicking on the `<None>` label, you are creating new content. There is not `Add New` button because every content is associated with an anchor and you can't create new content without attaching to an existing anchor. 

By clicking on other labels, you are modifying an existing content. 

*IMPORTANT: about how to use content editor* 

The content editor is loaded up to markdown library I found on Github. The functions don't quite fit in the application of this web app so I will write a custom editor in the future which should enable wordpress-like editing experience. So for now, writers should write there tutorials on a local document. And then copy paste it to the webpage. Uploading static files is a little bit inconvenient since it's separated process, but that's what I can do for now. 

You should use `Uplaods` page to upload static files and copy the relative link to the editor. Relative link is recommended and you should always use relative link. Every uploaded file will be available on `https://root_url/year/month/filename`, in this case `https://graphery.reedcompbio.org/year/month/filename`. It's writers duty to make sure the file name is not duplicated. 

The abstract box in the tutorial content will be rendered as html, so you can put either plain text or html there.

## Graph

In the graph editor, the can also see a url input and and name input. The same guideline from tutorial content editing should be applied here. You can paste the graph json to the text area or you can use the uploader below the text area to upload a json file and load the content by clicking the paper plane on the right. 

## Graph Info 

Nothing special about it. The *IMPORTANT* note in tutorial content section also applies here. 

## Code 

The code editor actually smashes two editors together. The top section is the actual code editor where you can paste the code and submit it. The second section is the result json generator. Since the server side generator is not complete yet, you can only use local generator, whose usage will be in a [separated page](/user-manual/local-server/index.html). One tutorial only has one page and you can only execute code on the graphs associated with that tutorial. 

You HAVE TO submit your code first and then generate json. There are two submit buttons for two section so MAKE SURE you saved both sections before exiting. 
