<template>
  <div class="markdown-body" v-html="processedHtml"></div>
</template>

<script>
  // TODO use custom css
  import 'mavon-editor/src/lib/css/md.css';
  import markdown from 'mavon-editor/src/lib/mixins/markdown';

  export default {
    props: {
      markdownRaw: {
        type: String,
        default: '',
      },
      inputHtml: {
        type: String,
        default: null,
      },
    },
    mixins: [markdown],
    methods: {
      loadLink(src) {
        const check = document.querySelectorAll("link[href='" + src + "']");
        if (check.length > 0) {
          return;
        }
        const link = document.createElement('link');
        const head = document.getElementsByTagName('head')[0];
        link.rel = 'stylesheet';
        link.href = src;
        head.appendChild(link);
      },
      loadScript(src) {
        const check = document.querySelectorAll("script[src='" + src + "']");
        if (check.length > 0) {
          return;
        }
        const script = document.createElement('script');
        const head = document.getElementsByTagName('head')[0];
        script.type = 'text/javascript';
        script.charset = 'UTF-8';
        script.src = src;
        head.appendChild(script);
      },
      hljsLang: function(lang) {
        return (
          'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/languages/' +
          lang +
          '.min.js'
        );
      },
      hljsCss: function(css) {
        return (
          'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/' +
          css +
          '.min.css'
        );
      },
    },
    computed: {
      processedHtml() {
        if (this.inputHtml !== null) {
          return this.inputHtml;
        }

        return this.markdownIt.render(this.markdownRaw);
      },
    },
    beforeMount() {
      // katex
      this.loadScript(
        'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.8.3/katex.min.js'
      );

      // highlight js
      this.loadScript(
        'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js'
      );

      // highlight lang
      this.loadScript(this.hljsLang('python'));

      // Markdown css
      this.loadLink(
        'https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/2.9.0/github-markdown.min.css'
      );

      // Highlighting css
      this.loadLink(this.hljsCss('vs'));

      // Katex css
      this.loadLink(
        'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.8.3/katex.min.css'
      );
    },
  };
</script>

<style lang="sass"></style>
