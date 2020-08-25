<script>
  export default {
    computed: {
      isCreatingNew() {
        return true;
      },
    },
    methods: {
      pushToNewPlace(id) {
        if (this.isCreatingNew) {
          this.$router.replace({ name: this.$route.name, params: { id } });
        }
      },
    },
  };
</script>
