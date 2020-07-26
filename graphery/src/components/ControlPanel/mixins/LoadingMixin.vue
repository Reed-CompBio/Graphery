<script>
  export default {
    data() {
      return {
        loadingContent: false,
      };
    },
    methods: {
      startLoading() {
        this.loadingContent = true;
      },
      finishedLoading() {
        this.loadingContent = false;
      },
    },
  };
</script>
