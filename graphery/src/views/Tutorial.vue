<template>
  <!-- make fill height class changable, then when graph  -->
  <div>
    <q-resize-observer @resize="resizeAction"></q-resize-observer>
    <q-splitter
      v-model="splitPos"
      :style="tutorialStyle"
      :horizontal="$q.screen.lt.md"
      separator-class="bg-light-blue"
      separator-style="width: 4px"
    >
      <template v-slot:before>
        <CytoscapeWrapper ref="cytoscapeWrapper"></CytoscapeWrapper>
      </template>
      <template v-slot:separator>
        <q-avatar
          color="primary"
          text-color="white"
          size="32px"
          icon="mdi-drag"
        />
      </template>
      <template v-slot:after>
        <TutorialArticle></TutorialArticle>
      </template>
    </q-splitter>
    <EditorWrapper
      v-show="editorShow && $q.screen.gt.xs"
      @close-editor="closeEditor"
      ref="editorWrapper"
    ></EditorWrapper>
    <q-page-sticky
      v-if="$q.screen.gt.xs"
      position="bottom-left"
      :offset="[30, 30]"
    >
      <q-btn round color="primary" icon="mdi-code-json" @click="toggleEditor" />
    </q-page-sticky>
  </div>
</template>

<script>
  import { headerSize } from '../store/states/meta';
  import { mapState } from 'vuex';

  export default {
    props: ['name'],
    components: {
      CytoscapeWrapper: () =>
        import('@/components/tutorial/CytoscapeWrapper.vue'),
      TutorialArticle: () =>
        import('@/components/tutorial/TutorialArticle.vue'),
      EditorWrapper: () => import('@/components/tutorial/EditorWrapper.vue'),
    },
    data() {
      return {
        editorShow: false,
      };
    },
    computed: {
      ...mapState('settings', ['graphSplitPos']),
      splitPos: {
        set(d) {
          this.$store.dispatch('settings/changeGraphSplitPos', d.toFixed(1));
        },
        get() {
          return this.graphSplitPos;
        },
      },
      tutorialStyle() {
        return {
          height: `calc(100vh - ${headerSize}px)`,
        };
      },
    },
    methods: {
      updateTutorialContent() {
        console.log('API calls to get details of the tutorial');
        // TODO
        // 1. API calls to get page conentent
        // 2. Extract articles and graph info, turn off loading for the article section and load article
        // 3. API calls using graph info to get graphs
        // 4. Extract graphs details , turn off loading for the graph section and load graphs
        // 5. (think about mini editor, how to manage the data in the backend)
      },
      toggleEditor() {
        this.editorShow = !this.editorShow;
      },
      closeEditor() {
        this.editorShow = false;
      },
      resizeAction() {
        // just ignore the error here
        this.$refs.editorWrapper.resizeEditorPos();
        this.$refs.cytoscapeWrapper.resizeGraph();
      },
    },
    watch: {
      name: function(newVal, oldVal) {
        // ensures page updating when the url is changed
        console.log(`route change from ${oldVal} to ${newVal}`);
        this.updateTutorialContent();
      },
    },
    mounted() {
      // pull tutorials
      this.$q.notify({
        multiLine: true,
        message: 'open code editor using {...} button',
        icon: 'mdi-code-json',
      });
      this.updateTutorialContent();
    },
  };
</script>
