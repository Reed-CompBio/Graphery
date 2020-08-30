const hljsLangs = { python: 'python', py: 'python', gyp: 'python' };

import markdownIt from 'markdown-it';

import emoji from 'markdown-it-emoji';
import sub from 'markdown-it-sub';
import sup from 'markdown-it-sup';
import deflist from 'markdown-it-deflist';
import abbr from 'markdown-it-abbr';
import footnote from 'markdown-it-footnote';
import insert from 'markdown-it-ins';
import mark from 'markdown-it-mark';
import taskLists from 'markdown-it-task-lists';
import container from 'markdown-it-container';
import katexExternal from 'markdown-it-katex-external';
import miip from 'markdown-it-images-preview';
import bp from './breakpoint';

// default mode
const markdownConfig = {
  html: true, // Enable HTML tags in source
  xhtmlOut: true, // Use '/' to close single tags (<br />).
  breaks: true, // Convert '\n' in paragraphs into <br>
  langPrefix: 'language-', // CSS language prefix for fenced blocks. Can be
  linkify: false, // 自动识别url
  typographer: true,
  quotes: '“”‘’',
  highlight: function(str, lang) {
    if (lang && hljsLangs[lang]) {
      return (
        '<pre><div class="hljs"><code class="' +
        lang +
        '">' +
        // eslint-disable-next-line @typescript-eslint/no-use-before-define
        markdown.utils.escapeHtml(str) +
        '</code></div></pre>'
      );
    }
    return (
      '<pre><code class="' +
      lang +
      '">' +
      // eslint-disable-next-line @typescript-eslint/no-use-before-define
      markdown.utils.escapeHtml(str) +
      '</code></pre>'
    );
  },
};

const markdown = markdownIt(markdownConfig);

// add target="_blank" to all link
const defaultRender =
  markdown.renderer.rules.link_open ||
  function(tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options);
  };
// eslint-disable-next-line @typescript-eslint/camelcase
markdown.renderer.rules.link_open = function(tokens, idx, options, env, self) {
  // If you are sure other plugins can't add `target` - drop check below
  const aIndex = tokens[idx].attrIndex('target');

  if (aIndex < 0) {
    tokens[idx].attrPush(['target', '_blank']); // add new attribute
  } else {
    tokens[idx].attrs[aIndex][1] = '_blank'; // replace value of existing attr
  }

  // pass token to default renderer.
  return defaultRender(tokens, idx, options, env, self);
};
// math katex
markdown
  .use(emoji)
  .use(taskLists)
  .use(sup)
  .use(sub)
  .use(container)
  .use(container, 'hljs-left') /* align left */
  .use(container, 'hljs-center') /* align center */
  .use(container, 'hljs-right') /* align right */
  .use(deflist)
  .use(abbr)
  .use(footnote)
  .use(insert)
  .use(mark)
  .use(container)
  .use(miip)
  .use(katexExternal)
  .use(bp);
export default markdown;
