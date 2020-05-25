<template>
  <!-- make fill height class changable, then when graph  -->
  <q-splitter :value="graphSplitPos" :style="tutorialStyle">
    <template v-slot:before>
      <CytoscapeWrapper></CytoscapeWrapper>
    </template>
    <template v-slot:after>
      <TutorialArticle></TutorialArticle>
    </template>
  </q-splitter>
</template>

<script>
  import { mapState } from 'vuex';

  export default {
    props: ['name'],
    components: {
      CytoscapeWrapper: () =>
        import('@/components/tutorial/CytoscapeWrapper.vue'),
      TutorialArticle: () =>
        import('@/components/tutorial/TutorialArticle.vue'),
    },
    computed: {
      ...mapState('meta', ['headerSize']),
      ...mapState('settings', ['graphSplitPos']),
      tutorialStyle() {
        return {
          height: `calc(100vh - ${this.headerSize}px)`,
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
