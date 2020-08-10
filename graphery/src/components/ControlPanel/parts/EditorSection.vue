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
  import { errorDialog } from '@/services/helpers';

  export default {
    props: {
      initValue: {
        type: String,
        default: '',
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
