<template>
  <div id="md-editor" class="full-height">
    <MonacoMarkdown
      language="en"
      :ishljs="true"
      ref="mdEditor"
      :init-value="initValue"
      class="full-height"
      @change="onChangeAction"
      @save="onSaveAction"
      @imgAdd="imgAddAction"
      @imgDel="imgDelAction"
    ></MonacoMarkdown>
  </div>
</template>

<script>
  import 'mavon-editor/dist/css/index.css';
  import { errorDialog } from '@/services/helpers';
  import MonacoMarkdown from '@/components/ControlPanel/parts/MarkdownEditor/MonacoMarkdown';

  export default {
    props: {
      initValue: {
        type: String,
        default: '',
      },
    },
    components: {
      MonacoMarkdown,
    },
    data() {
      return {
        rawText: '',
        splitPos: 50,
      };
    },
    methods: {
      imgAddAction() {
        errorDialog({
          message: 'Please use Uploads page to upload files.',
        });
      },
      imgDelAction() {
        errorDialog({
          message: 'Invalid Command!',
        });
      },
      getRawText() {
        return this.rawText;
      },
      initText(text) {
        if (this.initValue) {
          this.initValue = text;
        }
      },
      onChangeAction(value, render) {
        this.$emit('changes', value, render);
      },
      onSaveAction() {
        this.$emit('saves');
      },
      replaceUrl(pos, value) {
        this.$refs.mdEditor.$img2Url(pos, value);
      },
    },
  };
</script>

<style lang="sass">
  .markdown-editor-splitter .q-splitter
    height: 100%
</style>
