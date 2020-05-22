<template>
  <v-container fluid class="pb-3 fill-height tutorial-container">
    <v-row class="fill-height tutorial-row">
      <!-- this is for displaying graph -->
      <!-- cytoscape moubting point -->
      <CytoscapeWrapper class="tutorial-content"></CytoscapeWrapper>
      <TutorialArticle class="tutorial-content"></TutorialArticle>
    </v-row>
  </v-container>
</template>

<script>
  import CytoscapeWrapper from '@/components/tutorial/CytoscapeWrapper.vue';
  import TutorialArticle from '../components/tutorial/TutorialArticle';

  export default {
    props: ['name'],
    components: {
      CytoscapeWrapper,
      TutorialArticle,
    },
    data() {
      return {};
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
      this.updateTutorialContent();
    },
  };
</script>

<style scoped></style>
