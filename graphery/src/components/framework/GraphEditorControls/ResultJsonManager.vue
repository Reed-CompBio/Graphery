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
      getResultJsonPositionObject(positionId) {
        return this.resultJsonPositions[positionId];
      },
      getResultJsonPosition(positionId) {
        return this.resultJsonPositions[positionId].position;
      },
      updateResultJsonPosition(positionId, pos) {
        this.resultJsonPositions[positionId].position = pos;
      },
      initResultJsonPositions(graphIds, codeIds) {
        for (const graphId of graphIds) {
          for (const codeId of codeIds) {
            this.resultJsonPositions[
              this.getIdFromGraphIdAndCodeId(graphId, codeId)
            ] = { position: 1 };
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
