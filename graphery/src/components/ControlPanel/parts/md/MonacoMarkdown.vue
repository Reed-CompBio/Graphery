<template>
  <q-card>
    <div class="row full-width">
      <MarkdownToolbar class="full-width" />
    </div>
    <div class="row full-width" style="height: calc(100% - 32px);">
      <q-splitter
        v-model="splitterPos"
        class="full-width"
        :separator-class="'resizable-v-separator-splitter'"
      >
        <template v-slot:before>
          <Editor
            ref="editor"
            class="full-height"
            lang="markdown"
            :wrapLine="true"
            :miniMapEnable="true"
            :init-value="initValue"
            @editorContentChanged="onEditorContentChanged"
            @editorScrollChanged="onEditorScrollChanged"
          />
        </template>
        <template v-slot:separator>
          <SplitterSeparator />
        </template>
        <template v-slot:after>
          <div class="full-height full-width">
            <q-scroll-area
              class=" q-px-lg full-height full-width"
              ref="scrollArea"
            >
              <MarkdownSection
                class="q-my-lg"
                ref="markdownSection"
                :markdown-raw="rawMarkdown"
                :highlight="true"
                :render-breakpoint="true"
                @processedHtmlChanged="onProcessedHtmlChanged"
                @breakpointClicked="onBreakpointClicked"
              />
            </q-scroll-area>
          </div>
        </template>
      </q-splitter>
    </div>
  </q-card>
</template>
<script>
  import Editor from '@/components/framework/Editor';
  import MarkdownSection from '@/components/framework/MarkdownSection';
  import { successDialog } from '@/services/helpers';
  import { QScrollArea } from 'quasar';

  export default {
    props: {
      initValue: {
        type: String,
        default: '',
      },
    },
    components: {
      MarkdownSection,
      SplitterSeparator: () =>
        import('@/components/framework/SplitterSeparator'),
      MarkdownToolbar: () =>
        import('@/components/ControlPanel/parts/md/MarkdownToolbar'),
      Editor,
      QScrollArea,
    },
    data() {
      return {
        rawMarkdown: this.initValue,
        splitterPos: 60,
      };
    },
    methods: {
      onEditorContentChanged(content) {
        this.rawMarkdown = content;
      },
      onBreakpointClicked(position) {
        successDialog({
          message: `breakpoint clicked ${position}`,
        });
      },
      onProcessedHtmlChanged(processedHtml) {
        this.$emit('change', this.rawMarkdown, processedHtml);
      },
      onEditorScrollChanged(percentage) {
        // console.log('scroll to ', percentage);
      },
    },
    mounted() {
      if (this.$refs.editor) {
        this.$refs.editor.setCodeContent(this.initValue);
      }
    },
  };
</script>
