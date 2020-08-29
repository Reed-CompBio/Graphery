<template>
  <q-card>
    <q-card-section>
      Supported Markdown Syntax
      <q-btn
        color="grey"
        round
        flat
        dense
        :icon="expanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
        @click="expanded = !expanded"
      />
    </q-card-section>
    <q-slide-transition>
      <div v-show="expanded">
        <q-separator />
        <q-card-section>
          <MarkdownSection :markdown-raw="helpMarkdown" />
        </q-card-section>
      </div>
    </q-slide-transition>
  </q-card>
</template>
<script>
  import MarkdownSection from '@/components/framework/MarkdownSection';
  export default {
    components: { MarkdownSection },
    data() {
      return {
        helpMarkdown:
          'Markdown Guide\n' +
          '===\n' +
          '> Detailed: [http://commonmark.org/help/](http://commonmark.org/help/)\n' +
          '\n' +
          '## **Bold**\n' +
          '```\n' +
          '**bold**\n' +
          '__bold__\n' +
          '```\n' +
          '## *Italic*\n' +
          '```\n' +
          '*italic*\n' +
          '_italic_\n' +
          '```\n' +
          '## Header\n' +
          '```\n' +
          '# h1 #\n' +
          'h1\n' +
          '====\n' +
          '## h2 ##\n' +
          'h2\n' +
          '----\n' +
          '### h3 ###\n' +
          '#### h4 ####\n' +
          '##### h5 #####\n' +
          '###### h6 ######\n' +
          '```\n' +
          '## Dividing line\n' +
          '```\n' +
          '***\n' +
          '---\n' +
          '```\n' +
          '****\n' +
          '## ^Super^script & ~Sub~script\n' +
          '```\n' +
          'super x^2^\n' +
          'sub H~2~0\n' +
          '```\n' +
          '## ++Underline++ & ~~Strikethrough~~\n' +
          '```\n' +
          '++underline++\n' +
          '~~strikethrough~~\n' +
          '```\n' +
          '## ==Mark==\n' +
          '```\n' +
          '==mark==\n' +
          '```\n' +
          '## Quote\n' +
          '\n' +
          '```\n' +
          '> quote 1\n' +
          '>> quote 2\n' +
          '>>> quote 3\n' +
          '...\n' +
          '```\n' +
          '\n' +
          '## List\n' +
          '```\n' +
          'ol\n' +
          '1.\n' +
          '2.\n' +
          '3.\n' +
          '...\n' +
          '\n' +
          'ul\n' +
          '-\n' +
          '-\n' +
          '...\n' +
          '```\n' +
          '\n' +
          '## Todo List\n' +
          '\n' +
          '- [x] task 1\n' +
          '- [ ] task 2\n' +
          '\n' +
          '```\n' +
          '- [x] task 1\n' +
          '- [ ] task 2\n' +
          '```\n' +
          '\n' +
          '## Link\n' +
          '```\n' +
          'Text Link\n' +
          '[Text](www.baidu.com)\n' +
          '\n' +
          'Image Link\n' +
          '![Text](http://www.image.com)\n' +
          '```\n' +
          '## Code\n' +
          '\\``` type\n' +
          '\n' +
          'code block\n' +
          '\n' +
          '\\```\n' +
          '\n' +
          '\\` code \\`\n' +
          '\n' +
          '```python\n' +
          'def hello():\n' +
          "    print('hello world')\n" +
          '\n' +
          '```\n' +
          '`code`\n' +
          '\n' +
          '## Table\n' +
          '```\n' +
          '| th1 | th2 | th3 |\n' +
          '| :--  | :--: | ----: |\n' +
          '| left | center | right |\n' +
          '```\n' +
          '| th1 | th2 | th3 |\n' +
          '| :--  | :--: | ----: |\n' +
          '| left | center | right |\n' +
          '| ---------------------- | ------------- | ----------------- |\n' +
          '## Footnote\n' +
          '```\n' +
          'hello[^hello]\n' +
          '```\n' +
          '\n' +
          'Look at the bottom[^hello]\n' +
          '\n' +
          '[^hello]: footnote\n' +
          '\n' +
          '## Emojis\n' +
          'Detailed: [https://www.webpagefx.com/tools/emoji-cheat-sheet/](https://www.webpagefx.com/tools/emoji-cheat-sheet/)\n' +
          '```\n' +
          ':laughing:\n' +
          ':blush:\n' +
          ':smiley:\n' +
          ':)\n' +
          '...\n' +
          '```\n' +
          ':laughing::blush::smiley::)\n' +
          '\n' +
          '## $\\KaTeX$ Mathematics\n' +
          '\n' +
          'We can render formulas for example：$x_i + y_i = z_i$ and $\\sum_{i=1}^n a_i=0$\n' +
          'We can also single-line rendering\n' +
          '$$\\sum_{i=1}^n a_i=0$$\n' +
          'Detailed: [katex](http://www.intmath.com/cg5/katex-mathjax-comparison.php)和[katex function](https://github.com/Khan/KaTeX/wiki/Function-Support-in-KaTeX)以及[latex](https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference)\n' +
          '\n' +
          '## Layout\n' +
          '\n' +
          '::: hljs-left\n' +
          '`::: hljs-left`\n' +
          '`left`\n' +
          '`:::`\n' +
          ':::\n' +
          '\n' +
          '::: hljs-center\n' +
          '`::: hljs-center`\n' +
          '`center`\n' +
          '`:::`\n' +
          ':::\n' +
          '\n' +
          '::: hljs-right\n' +
          '`::: hljs-right`\n' +
          '`right`\n' +
          '`:::`\n' +
          ':::\n' +
          '\n' +
          '## deflist\n' +
          '\n' +
          'Term 1\n' +
          '\n' +
          ':   Definition 1\n' +
          '\n' +
          'Term 2 with *inline markup*\n' +
          '\n' +
          ':   Definition 2\n' +
          '\n' +
          '        { some code, part of Definition 2 }\n' +
          '\n' +
          '    Third paragraph of definition 2.\n' +
          '\n' +
          '```\n' +
          'Term 1\n' +
          '\n' +
          ':   Definition 1\n' +
          '\n' +
          'Term 2 with *inline markup*\n' +
          '\n' +
          ':   Definition 2\n' +
          '\n' +
          '        { some code, part of Definition 2 }\n' +
          '\n' +
          '    Third paragraph of definition 2.\n' +
          '\n' +
          '```\n' +
          '\n' +
          '## abbr\n' +
          '*[HTML]: Hyper Text Markup Language\n' +
          '*[W3C]:  World Wide Web Consortium\n' +
          'The HTML specification\n' +
          'is maintained by the W3C.\n' +
          '```\n' +
          '*[HTML]: Hyper Text Markup Language\n' +
          '*[W3C]:  World Wide Web Consortium\n' +
          'The HTML specification\n' +
          'is maintained by the W3C.\n' +
          '```\n' +
          '## breakpoint\n' +
          '`@number@` => `@12@`\n' +
          '@12@',
        expanded: false,
      };
    },
  };
</script>
