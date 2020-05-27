<template>
  <!-- make fill height class changable, then when graph  -->
  <div>
    <q-splitter
      :value="splitPos"
      :style="tutorialStyle"
      :horizontal="$q.screen.lt.md"
      separator-class="bg-light-blue"
      separator-style="width: 4px"
    >
      <template v-slot:before>
        <CytoscapeWrapper></CytoscapeWrapper>
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
        editorShow: true,
      };
    },
    computed: {
      ...mapState('settings', ['graphSplitPos']),
      splitPos: {
        set(d) {
          this.$store.dispatch('changeSepPos', d);
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
      this.updateTutorialContent();
    },
  };
</script>
