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
          console.log(this.$route.name);
          this.$router.push({ name: this.$route.name, params: { id } });
        }
      },
    },
  };
</script>
