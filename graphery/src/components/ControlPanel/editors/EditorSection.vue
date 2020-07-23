<template>
  <div id="md-editor" class="full-height">
    <mavonEditor
      language="en"
      :ishljs="true"
      ref="mdEditor"
      :value="initValue"
      class="full-height"
    ></mavonEditor>
  </div>
</template>

<script>
  import { mavonEditor } from 'mavon-editor';
  import 'mavon-editor/dist/css/index.css';

  export default {
    components: {
      mavonEditor,
    },
    data() {
      return {
        rawText: '',
        splitPos: 50,
        initValue: '',
      };
    },
    methods: {
      getRawText() {
        return this.rawText;
      },
      getProcessedHtml() {
        return this.$refs.markdownSection.getProcessedHtml();
      },
    },
  };
</script>

<style lang="sass">
  .markdown-editor-splitter .q-splitter
    height: 100%
</style>
