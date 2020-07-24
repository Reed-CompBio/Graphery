<script>
  export default {
    data() {
      return {
        loadingTable: false,
      };
    },
    methods: {
      startLoading() {
        this.loadingTable = true;
      },
      finishedLoading() {
        this.loadingTable = false;
      },
    },
  };
</script>
