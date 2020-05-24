<template>
  <!-- make fill height class changable, then when graph  -->
  <q-page-container class="fill-height">
    <q-splitter class="fill-height" :value="graphSplitPos">
      <template v-slot:before class="fill-height">
        <CytoscapeWrapper></CytoscapeWrapper>
      </template>
      <template v-slot:after>
        <!--        <TutorialArticle style="max-height: 100%"></TutorialArticle>-->
      </template>
    </q-splitter>
  </q-page-container>
</template>

<script>
  import CytoscapeWrapper from '@/components/tutorial/CytoscapeWrapper.vue';
  import TutorialArticle from '../components/tutorial/TutorialArticle';
  import { mapState } from 'vuex';

  export default {
    props: ['name'],
    components: {
      CytoscapeWrapper,
      // TutorialArticle,
    },
    data() {
      return {
        containerHeight: null,
      };
    },
    computed: {
      ...mapState('settings', ['graphSplitPos']),
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
        "v-container's height:"
        // document.getElementById('tutorial-container').clientHeight
      );

      // after retrieving the height of the component, pull tutorials
      // so that I can get
      this.updateTutorialContent();
    },
  };
</script>

<style scoped></style>
