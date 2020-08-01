<template>
  <div class="markdown-body" v-html="processedHtml"></div>
</template>

<script>
  // TODO use custom css
  import 'mavon-editor/src/lib/css/md.css';
  import markdown from 'mavon-editor/src/lib/core/markdown';
  import hljs from 'highlight.js/lib/core';
  import python from 'highlight.js/lib/languages/python.js';
  import github from 'highlight.js/styles/github.css';

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
        markdownIt: markdown,
      };
    },
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
      loadExternalResources() {
        // katex
        this.loadScript(
          'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.8.3/katex.min.js',
          () => {
            this.renderHtml();
          }
        );
        // Markdown css
        this.loadLink(
          'https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css'
        );

        // Katex css
        this.loadLink(
          'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.8.3/katex.min.css'
        );
      },
      highlightCode() {
        document.querySelectorAll('pre div.hljs code').forEach((block) => {
          hljs.highlightBlock(block);
        });
      },
      renderHtml() {
        this.renderedHtml = this.markdownIt.render(this.markdownRaw);
        this.highlightCode();
        // this.$render(this.markdownRaw, (res) => {
        //   this.renderedHtml = res;
        // });
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
      hljs.registerLanguage('python', python);
      this.loadExternalResources();
    },
    watch: {
      // TODO merge this into a computed value
      markdownRaw: function() {
        this.renderHtml();
      },
    },
  };
</script>

<style lang="sass">
  pre
    box-shadow: 0 1px 5px rgba(0,0,0,0.2), 0 2px 2px rgba(0,0,0,0.14), 0 3px 1px -2px rgba(0,0,0,0.12)
  pre > .hljs
    font-size: 1rem !important
    background-color: #f6f8fa
</style>
