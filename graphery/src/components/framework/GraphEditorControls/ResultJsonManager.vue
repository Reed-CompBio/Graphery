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
      initResultJsonPositions(codeIds, graphIds) {
        for (const graphId of graphIds) {
          for (const codeId of codeIds) {
            this.resultJsonPositions[
              this.getIdFromGraphIdAndCodeId(graphId, codeId)
            ] = 1;
          }
        }
      },
    },
  };
</script>
