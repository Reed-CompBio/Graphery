<template>
  <div
    class="markdown-body"
    ref="markdownMountingPoint"
    v-html="processedHtml"
  ></div>
</template>

<script>
  import markdown from '@/components/ControlPanel/parts/md/markdown';
  import hljs from 'highlight.js/lib/core';
  import python from 'highlight.js/lib/languages/python.js';

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
      highlight: {
        type: Boolean,
        default: false,
      },
      breakpointReact: {
        type: Boolean,
        default: false,
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
        if (typeof callback !== 'function') {
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
        if (typeof callback !== 'function') {
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
          'https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js',
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
          'https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css'
        );
      },
      highlightCode() {
        document.querySelectorAll('pre div.hljs code').forEach((block) => {
          hljs.highlightBlock(block);
        });
      },
      renderHtml() {
        this.renderedHtml = this.markdownIt.render(this.markdownRaw);
        // this.$render(this.markdownRaw, (res) => {
        //   this.renderedHtml = res;
        // });
      },
      replaceBreakpoints() {
        for (const tag of this.$refs.markdownMountingPoint.getElementsByClassName(
          'tutorial-breakpoint'
        )) {
          console.log(tag);
          tag.addEventListener('click', (event) => {
            this.$emit(
              'breakpointClicked',
              event.target.getAttribute('position')
            );
          });
        }
      },
      postRenderProcessing() {
        this.$nextTick(() => {
          if (this.highlight) {
            this.highlightCode();
          }
          if (this.breakpointReact) {
            this.replaceBreakpoints();
          }
        });
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
    beforeMount() {
      hljs.registerLanguage('python', python);
      hljs.initHighlightingOnLoad();
      this.loadExternalResources();
    },
    mounted() {
      this.postRenderProcessing();
    },
    watch: {
      // TODO merge this into a computed value
      markdownRaw: function() {
        this.renderHtml();
      },
      processedHtml: function() {
        this.$emit('processedHtmlChanged', this.processedHtml);
        this.postRenderProcessing();
      },
    },
  };
</script>

<style lang="sass">
  @import "~highlight.js/styles/github.css"
  .markdown-body pre
    box-shadow: 0 1px 5px rgba(0,0,0,0.2), 0 2px 2px rgba(0,0,0,0.14), 0 3px 1px -2px rgba(0,0,0,0.12)
  .markdown-body pre > .hljs
    font-size: 1rem !important
    background-color: #f6f8fa

  .markdown-body span.tutorial-breakpoint
    padding: 2px
    background-color: #00acc1
    border-radius: 30px
    cursor: pointer

  .markdown-body strong
    font-weight: bolder
  .markdown-body .hljs-center
      text-align: center
  .markdown-body .hljs-right
      text-align: right
  .markdown-body .hljs-left
      text-align: left
</style>
