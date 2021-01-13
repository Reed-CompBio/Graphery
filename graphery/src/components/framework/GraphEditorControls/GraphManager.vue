<script>
  import { mapGetters } from 'vuex';

  export default {
    computed: {
      ...mapGetters('graphs', ['getCurrentGraphId', 'getCurrentGraphObject']),
      currentGraphId: {
        set(d) {
          this.$store.commit('graphs/LOAD_CURRENT_GRAPH_ID', d);
        },
        get() {
          return this.getCurrentGraphId;
        },
      },
      currentGraphObject() {
        return this.getCurrentGraphObject;
      },
    },
    methods: {
      loadGraphObjectListFromMatched(graphList) {
        this.$store.commit('graphs/LOAD_GRAPH_OBJECT_LIST', graphList);
      },
    },
  };
</script>
