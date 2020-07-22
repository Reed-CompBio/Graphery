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
    data() {
      return {
        renderedHtml: '',
      };
    },
    mixins: [markdown],
    methods: {
      loadLink(src, callback) {
        if (!(typeof callback === 'function')) {
          callback = function() {
            return null;
          };
        }

        const check = document.querySelectorAll("link[href='" + src + "']");
        if (check.length > 0) {
          callback();
          return;
        }
        const link = document.createElement('link');
        const head = document.getElementsByTagName('head')[0];
        link.rel = 'stylesheet';
        link.href = src;
        if (link.addEventListener) {
          link.addEventListener(
            'load',
            function() {
              callback();
            },
            false
          );
        } else if (link.attachEvent) {
          link.attachEvent('onreadystatechange', function() {
            const target = window.event.srcElement;
            if (target.readyState === 'loaded') {
              callback();
            }
          });
        }
        head.appendChild(link);
      },
      loadScript(src, callback) {
        if (!(typeof callback === 'function')) {
          callback = function() {
            return null;
          };
        }

        const check = document.querySelectorAll("script[src='" + src + "']");
        if (check.length > 0) {
          check[0].addEventListener('load', function() {
            callback();
          });
          callback();
          return;
        }
        const script = document.createElement('script');
        const head = document.getElementsByTagName('head')[0];
        script.type = 'text/javascript';
        script.charset = 'UTF-8';
        script.src = src;

        if (script.addEventListener) {
          script.addEventListener(
            'load',
            function() {
              callback();
            },
            false
          );
        } else if (script.attachEvent) {
          script.attachEvent('onreadystatechange', function() {
            const target = window.event.srcElement;
            if (target.readyState === 'loaded') {
              callback();
            }
          });
        }

        head.appendChild(script);
      },
      hljsLang: function(lang) {
        return (
          'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/languages/' +
          lang +
          '.min.js'
        );
      },
      hljsCss(css) {
        return (
          'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/' +
          css +
          '.min.css'
        );
      },
      loadExternalResources() {
        // katex
        this.loadScript(
          'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.8.3/katex.min.js',
          () => {
            this.renderHtml();
          }
        );

        // highlight js
        this.loadScript(
          'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js',
          () => {
            this.renderHtml();
          }
        );

        // Markdown css
        this.loadLink(
          'https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/2.9.0/github-markdown.min.css'
        );

        // Highlighting css
        this.loadLink(this.hljsCss('github'));

        // Katex css
        this.loadLink(
          'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.8.3/katex.min.css'
        );
      },
      renderHtml() {
        this.renderedHtml = this.markdownIt.render(this.markdownRaw);
      },
    },
    computed: {
      processedHtml() {
        if (this.inputHtml !== null) {
          return this.inputHtml;
        }

        return this.renderedHtml;
      },
    },
    mounted() {
      this.loadExternalResources();
      this.renderHtml();
    },
    watch: {
      // TODO merge this into a computed value
      markdownRaw: function() {
        this.renderedHtml();
      },
    },
  };
</script>

<style lang="sass"></style>
