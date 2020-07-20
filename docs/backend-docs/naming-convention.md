# Naming Convention

## CLI Reader Folder

<!-- TODO change the title name -->

The folder structure should be structured as following:

```
.
└── One Tutorial
    ├── code
    │   ├── entry.py
    │   ├── graph-info.json
    │   ├── other_modules.py
    │   └── ...
    ├── graphs
    │   ├── graph1.json
    │   ├── graph2.json
    │   └── ...
    └── locale
        ├── statics
        │   ├── example.jpg
        │   └── ...
        ├── title.en-us.md
        ├── title.zh-cn.md
        └── ...
```

<!--
# One Tutorial
## code
### entry.py
### graph-info.json
### other_modules.py
### ... 
## graphs
### graph1.json
### graph2.json
### ...
## locale
### statics
#### example.jpg
#### ...
### title.en-us.md
### title.zh-cn.md
### ...
-->

The `Root_Foler` contains everything that's need to generate a tutorial page.

The resources are divided into three parts: code, graphs, and locale. We will go through them one by one. 

## `code` Folder 

The code folder contains all the python code required by this tutorial. Multiple-module/file management is not supported yet. So right now, all the code should be written in one file, the `entry.py` file. The CLI will detect `entry.py` file and import the code in it. In side `entry.py` file, there ***must*** be a `main` function, that is 

```python
def main():
    # do something
```

The function has ***no*** arguments and returns `None`. The CLI will look for `main` and use it to start the program. Therefore, you can add other functions in `entry.py` and make sure you reference it directly or indirectly from `main`.

We have a `sight` module located in `bundle.sight`, from which you can import `tracer`. `tracer` can be used as a function decorator and it traces the variable changes inside of the function. For more usages on `tracer`, check out the `README.md` file and the `ADVANCED_USAGE.md` file in the GitHub repo. 

If you want to use graph objects in the code, make sure the graph is already registered in the database. To reference a registered graph, you can use `graph-info.json`. There are two fields in the file, `required_graphs` and `from_tutorials`. Both of them must be list of strings of url (to be changed in the future) pointing to the graph object. To use the graph in the code, you ***must*** import the `graph_object` variable under `bundle.utils.dummy_graph` module. You should use it instead of creating your own graph object, since the CLI will swap the value of `graph_object` with actual graph objects stated in `graph-info.json`. 

## `graphs` Folder

The graph folder contains the jsons of the graphs you want to upload to the database. They must follow cyjs format. More about cyjs, please check out this [link](https://js.cytoscape.org/#notation/elements-json) (the second example in that section). 

The name of the graph json file will be used as the `name` of the graph, which is a unique identified in the database. The `url` of the graph will simply be `name` with every `<space>` replaced by `-`. However, you can change them in the CLI to any strings you want. 

Additionally, every graph has a short abstract and a human readable title. Each translation of a description should be stored in a Markdown file whose file name follows the Markdown file naming convention below. In addition to the conventions below, the graph abstract should only have one paragraph, that is, one line of content in the markdown file. The extra lines will be omitted. 

## `locale` Folder

The `locale` folder contains the actual content of the tutorials. Each translation of the actual content should be stored in a Markdown file, whose file name also follows the Markdown file naming convention. 

The `abstract` of the content in that translation will be the fist paragraph of the actual content. You can modify it in the CLI or in the admin page. 

The statics folder under the `locale` folder should contain any static objects used in the Markdown translation, like images for example. 

## Markdown File Convention

The Markdown file should be named in `title.language_code.md`. The title will be the default `title` prompted by CLI. You can of course modify it. The language code should be the code of the following supported language:

* `en-us`
* `zh-cn`

Note that even English is counted as a translation. So you cannot omit the language code of an English MD file. 

The Markdown file may have one and only one `<h1>` tag, which is `#` in Markdown format. It will be removed during processing and will be the default `title` prompted by CLI. 
