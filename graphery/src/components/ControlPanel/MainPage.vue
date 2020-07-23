<template>
  <ControlPanelContentFrame>
    <template slot="title"> Welcome {{ userObj.username }} </template>
    <template>
      <div class="text-h4">
        <p>
          There ain't much you can do in this page, but I promise I will add
          more fun.
        </p>
      </div>
      <MarkdownSection :markdownRaw="exampleMd"></MarkdownSection>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { mapState } from 'vuex';

  export default {
    data() {
      return {
        exampleMd:
          '# h1 Heading 8-)\n' +
          '## h2 Heading\n' +
          '### h3 Heading\n' +
          '#### h4 hhh\n' +
          '##### h5 hhhhh\n' +
          '<h2> h2 Heading by HTML</h2>\n' +
          '\n' +
          '## Horizontal Rules\n' +
          ' $\\sqrt{2}$ 1' +
          '\n' +
          '___\n' +
          '\n' +
          '---\n' +
          '\n' +
          '***\n' +
          '\n' +
          '## Typographic replacements\n' +
          '\n' +
          'Enable typographer option to see result.\n' +
          '\n' +
          '(c) (C) (r) (R) (tm) (TM) (p) (P) +-\n' +
          '\n' +
          'test.. test... test..... test?..... test!....\n' +
          '\n' +
          '!!!!!! ???? ,,  -- ---\n' +
          '\n' +
          '"Smartypants, double quotes" and \'single quotes\'\n' +
          '\n' +
          '\n' +
          '## Emphasis\n' +
          '\n' +
          '**This is bold text**\n' +
          '\n' +
          '__This is bold text__\n' +
          '\n' +
          '*This is italic text*\n' +
          '\n' +
          '_This is italic text_\n' +
          '\n' +
          '~~Strikethrough~~\n' +
          '\n' +
          '\n' +
          '## Blockquotes\n' +
          '\n' +
          '\n' +
          '> Blockquotes can also be nested...\n' +
          '>> ...by using additional greater-than signs right next to each other...\n' +
          '> > > ...or with spaces between arrows.\n' +
          '\n' +
          '\n' +
          '## Lists\n' +
          '\n' +
          'Unordered\n' +
          '\n' +
          '+ Create a list by starting a line with `+`, `-`, or `*`\n' +
          '+ Sub-lists are made by indenting 2 spaces:\n' +
          '  - Marker character change forces new list start:\n' +
          '    * Ac tristique libero volutpat at\n' +
          '    + Facilisis in pretium nisl aliquet\n' +
          '    - Nulla volutpat aliquam velit\n' +
          '+ Very easy!\n' +
          '\n' +
          'Ordered\n' +
          '\n' +
          '1. Lorem ipsum dolor sit amet\n' +
          '2. Consectetur adipiscing elit\n' +
          '3. Integer molestie lorem at massa\n' +
          '\n' +
          '\n' +
          '1. You can use sequential numbers...\n' +
          '1. ...or keep all the numbers as `1.`\n' +
          '\n' +
          'Start numbering with offset:\n' +
          '\n' +
          '57. foo\n' +
          '1. bar\n' +
          '\n' +
          '\n' +
          '## Code\n' +
          '\n' +
          'Inline `code`\n' +
          '\n' +
          'Indented code\n' +
          '\n' +
          '    // Some comments\n' +
          '    line 1 of code\n' +
          '    line 2 of code\n' +
          '    line 3 of code\n' +
          '\n' +
          '\n' +
          'Block code "fences"\n' +
          '\n' +
          '```\n' +
          'Sample text here...\n' +
          '```\n' +
          'Syntax highlighting\n' +
          '\n' +
          '```python\n' +
          'def hello():\n' +
          '    print("hello world")\n' +
          '    return None\n' +
          '\n' +
          '```\n' +
          '\n' +
          '\n' +
          '## Tables\n' +
          '\n' +
          '| Option | Description |\n' +
          '| ------ | ----------- |\n' +
          '| data   | path to data files to supply the data that will be passed into templates. |\n' +
          '| engine | engine to be used for processing templates. Handlebars is the default. |\n' +
          '| ext    | extension to be used for dest files. |\n' +
          '\n' +
          'Right aligned columns\n' +
          '\n' +
          '| Option | Description |\n' +
          '| ------:| -----------:|\n' +
          '| data   | path to data files to supply the data that will be passed into templates. |\n' +
          '| engine | engine to be used for processing templates. Handlebars is the default. |\n' +
          '| ext    | extension to be used for dest files. |\n' +
          '\n' +
          '## Links\n' +
          '\n' +
          '[vue-markdown](https://github.com/miaolz123/vue-markdown)\n' +
          '\n' +
          '[link with title](https://github.com/miaolz123/vue-markdown "VueMarkdown")\n' +
          '\n' +
          'Autoconverted link https://github.com/miaolz123/vue-markdown (enable linkify to see)\n' +
          '\n' +
          '\n' +
          '## Images\n' +
          '\n' +
          '![Minion](dist/img/minion.png)\n' +
          '\n' +
          'Like links, Images also have a footnote style syntax\n' +
          '\n' +
          '![Alt text][id]\n' +
          '\n' +
          'With a reference later in the document defining the URL location:\n' +
          '\n' +
          '[id]: dist/img/minion.png  "The Dojocat"\n' +
          '\n' +
          '\n' +
          '### Emojies\n' +
          '\n' +
          '> Classic markup: :wink: :cry: :laughing: :yum:\n' +
          '>\n' +
          '> Shortcuts (emoticons): :-) :-( 8-) ;)\n' +
          '\n' +
          '\n' +
          '### Subscript / Superscript\n' +
          '\n' +
          '- 19^th^\n' +
          '- H~2~O\n' +
          '\n' +
          '\n' +
          '### \\<ins>\n' +
          '\n' +
          '++Inserted text++\n' +
          '\n' +
          '\n' +
          '### \\<mark>\n' +
          '\n' +
          '==Marked text==\n' +
          '\n' +
          '\n' +
          '### Footnotes\n' +
          '\n' +
          'Footnote 1 link[^first].\n' +
          '\n' +
          'Footnote 2 link[^second].\n' +
          '\n' +
          'Inline footnote^[Text of inline footnote] definition.\n' +
          '\n' +
          'Duplicated footnote reference[^second].\n' +
          '\n' +
          '[^first]: Footnote **can have markup**\n' +
          '\n' +
          '    and multiple paragraphs.\n' +
          '\n' +
          '[^second]: Footnote text.\n' +
          '\n' +
          '\n' +
          '### Definition lists\n' +
          '\n' +
          'Term 1\n' +
          '\n' +
          ':   Definition 1\n' +
          'with lazy continuation.\n' +
          '\n' +
          'Term 2 with *inline markup*\n' +
          '\n' +
          ':   Definition 2\n' +
          '\n' +
          '        { some code, part of Definition 2 }\n' +
          '\n' +
          '    Third paragraph of definition 2.\n' +
          '\n' +
          '_Compact style:_\n' +
          '\n' +
          'Term 1\n' +
          '  ~ Definition 1\n' +
          '\n' +
          'Term 2\n' +
          '  ~ Definition 2a\n' +
          '  ~ Definition 2b\n' +
          '\n' +
          '\n' +
          '### Abbreviations\n' +
          '\n' +
          'This is HTML abbreviation example.\n' +
          '\n' +
          'It converts "HTML", but keep intact partial entries like "xxxHTMLyyy" and so on.\n' +
          '\n' +
          '*[HTML]: Hyper Text Markup Language',
      };
    },
    components: {
      ControlPanelContentFrame: () => import('./ControlPanelContentFrame.vue'),
      MarkdownSection: () => import('./MarkdownSection.vue'),
    },
    computed: {
      ...mapState({
        userObj: (state) => state.user,
      }),
    },
  };
</script>
