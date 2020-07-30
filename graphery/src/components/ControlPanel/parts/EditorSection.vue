<template>
  <div id="md-editor" class="full-height">
    <mavonEditor
      language="en"
      :ishljs="true"
      ref="mdEditor"
      :value="initValue"
      class="full-height"
      @change="onChangeAction"
      @imgAdd="imgAddAction"
      @imgDel="imgDelAction"
    ></mavonEditor>
  </div>
</template>

<script>
  import { mavonEditor } from 'mavon-editor';
  import 'mavon-editor/dist/css/index.css';

  export default {
    props: {
      imgAddAction: {
        type: Function,
      },
      imgDelAction: {
        type: Function,
      },
    },
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
      initText(text) {
        this.initValue = text;
      },
      onChangeAction(value, render) {
        this.$emit('changes', value, render);
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
