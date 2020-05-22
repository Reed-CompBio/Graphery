<template>
  <div id="cy"></div>
</template>

<script>
  import cytoscape from 'cytoscape';

  export default {
    data() {
      return {
        cyInstance: null,
      };
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
