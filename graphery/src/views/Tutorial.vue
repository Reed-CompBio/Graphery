<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <!-- this is for displaying graph -->
        <div>
          <!-- cytoscape mouting point -->
          <CytoscapeWrapper></CytoscapeWrapper>
        </div>
      </v-col>
      <v-col>
        <div id="article"></div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import CytoscapeWrapper from '@/components/tutorial/CytoscapeWrapper.vue';

  export default {
    props: ['name'],
    components: {
      CytoscapeWrapper,
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
