<script>
  import { mapGetters } from 'vuex';
  export default {
    data() {
      return {
        resultJsonPositions: {},
      };
    },
    computed: {
      ...mapGetters('rj', ['getCurrentJsonObject', 'getCurrentJsonString']),
    },
    methods: {
      getIdFromGraphIdAndCodeId(graphId, codeId) {
        return `${graphId}-${codeId}`;
      },
      updateResultJsonPosition(graphId, codeId, pos) {
        this.resultJsonPositions[
          this.getIdFromGraphIdAndCodeId(graphId, codeId)
        ] = pos;
      },
      initResultJsonPositions(graphIds, codeIds) {
        for (const graphId of graphIds) {
          for (const codeId of codeIds) {
            this.resultJsonPositions[
              this.getIdFromGraphIdAndCodeId(graphId, codeId)
            ] = 1;
          }
        }
      },
      loadResultJsonListFromQueryData(jsonList) {
        this.$store.dispatch('rj/loadResultJsonListFromQueryData', jsonList);
      },
      loadResultJsonListFromMatched(jsonList) {
        this.$store.dispatch('rj/loadResultJsonListFromMatched', jsonList);
      },
    },
  };
</script>
