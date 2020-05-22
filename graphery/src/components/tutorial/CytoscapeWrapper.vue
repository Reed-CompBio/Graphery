<template>
  <div id="cy"></div>
</template>

<script>
  import cytoscape from 'cytoscape';
  import { mapGetters } from 'vuex';

  export default {
    data() {
      return {
        cyInstance: null,
        selector: 0, // used in drop menu to select graphs
      };
    },
    computed: {
      ...mapGetters('tutorials', [
        'getGraphById',
        'getGraphByIndex',
        'articleEmpty',
        'graphsEmpty',
        'codesEmpty',
      ]),
      currentGraph() {
        return this.getGraphByIndex(this.selector);
      },
      currentGraphId() {
        return this.currentGraph | this.currentGraph.id; // can't remember the syntax here
      },
      currentGraphJson() {
        return this.currentGraph | this.currentGraph.cyjs;
      },
    },
    mounted() {
      this.cyInstance = Object.freeze(
        cytoscape({
          container: document.getElementById('cy'),
        })
      );

      console.log('cy obj is mounted', this.cyInstance);
    },
  };
</script>
