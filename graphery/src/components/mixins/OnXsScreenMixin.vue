<script>
  export default {
    computed: {
      onXsScreen() {
        return this.$q.screen.lt.sm;
      },
    },
  };
</script>
