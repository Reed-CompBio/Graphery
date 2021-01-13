<template>
  <div
    class="markdown-body"
    ref="markdownMountingPoint"
    v-html="processedHtml"
  ></div>
</template>

<script>
  import markdown from '@/components/framework/md/markdown';

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
      pictureZoom: {
        type: Boolean,
        default: false,
      },
      docId: {
        type: String,
        default: 'default',
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

        // Katex css
        this.loadLink(
          'https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css'
        );
      },
      renderHtml() {
        this.renderedHtml = this.markdownIt.render(this.markdownRaw, {
          docId: this.docId,
        });
        // this.$render(this.markdownRaw, (res) => {
        //   this.renderedHtml = res;
        // });
      },
      replaceBreakpoints() {
        for (const tag of this.$refs.markdownMountingPoint.getElementsByClassName(
          'tutorial-breakpoint'
        )) {
          tag.addEventListener('click', (event) => {
            this.$emit(
              'breakpointClicked',
              event.target.getAttribute('position')
            );
          });
        }
      },
      processPictureZoom() {
        const picList = [];
        for (const tag of this.$refs.markdownMountingPoint.getElementsByTagName(
          'img'
        )) {
          picList.push(tag.getAttribute('src'));

          tag.addEventListener('click', (event) => {
            this.$emit('pictureZoomRequest', event.target.getAttribute('src'));
          });

          tag.classList.add('picture-zoom-ready');
        }
        this.$emit('updatePictureSrcList', picList);
      },
      postRenderProcessing() {
        this.$nextTick(() => {
          if (this.breakpointReact) {
            this.replaceBreakpoints();
          }
          if (this.pictureZoom) {
            this.processPictureZoom();
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
        this.postRenderProcessing();
        this.$emit('processedHtmlChanged', this.processedHtml);
      },
    },
  };
</script>

<style lang="sass">
  @import "~highlight.js/styles/github.css"
  @import "~@/styles/github-markdown.min.css"
  @import "~@/styles/markdown.sass"
</style>
