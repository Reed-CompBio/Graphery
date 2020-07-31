<template>
  <div id="md-editor" class="full-height">
    <mavonEditor
      language="en"
      :ishljs="true"
      ref="mdEditor"
      :value="initValue"
      class="full-height"
      @change="onChangeAction"
      @save="onSaveAction"
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
      initValue: {
        type: String,
        default: '',
      },
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
      };
    },
    methods: {
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
