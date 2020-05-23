<template>
  <!-- make fill height class changable, then when graph  -->
  <v-container fluid class="pb-5 fill-height" id="tutorial-container">
    <v-row class="fill-height">
      <!-- this is for displaying graph -->
      <v-col class="fill-height" cols="6">
        <!-- cytoscape moubting point -->
        <CytoscapeWrapper class="tutorial-content"></CytoscapeWrapper>
      </v-col>

      <v-col cols="6" style="max-height: 100%">
        <TutorialArticle class="tutorial-content"></TutorialArticle>
      </v-col>
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
      return {
        containerHeight: null,
      };
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
      setupContainerHeight(height) {
        this.containerHeight = height;
      },
      onWindowResize() {
        // get height
        let height;
        this.setupContainerHeight(height);
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
      // When the container is mounted, get the height of the container, then set the height so that it won't change
      console.log(
        "v-container's height:",
        document.getElementById('tutorial-container').clientHeight
      );

      // after retrieving the height of the component, pull tutorials
      // so that I can get
      this.updateTutorialContent();
    },
  };
</script>

<style scoped></style>
