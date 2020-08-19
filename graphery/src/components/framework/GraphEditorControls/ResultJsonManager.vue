<script>
  import { mapGetters } from 'vuex';
  export default {
    computed: {
      ...mapGetters('rj', [
        'getCurrentJsonObject',
        'getCurrentJsonString',
        'getResultJsonObjectElement',
        'getResultJsonPositionFromId',
        'getResultJsonPositionObjectFromId',
      ]),
    },
    methods: {
      getIdFromGraphIdAndCodeId(graphId, codeId) {
        return `${graphId}-${codeId}`;
      },
      getResultJsonPositionObject(positionId) {
        return this.getResultJsonPositionObjectFromId(positionId);
      },
      getResultJsonPosition(positionId) {
        return this.getResultJsonPositionFromId(positionId);
      },
      updateResultJsonPosition(positionId, position) {
        this.$store.commit('rj/CHANGE_JSON_LOCATION', { positionId, position });
      },
      initResultJsonPositions(graphIds, codeIds) {
        const resultJsonPositions = {};
        for (const graphId of graphIds) {
          for (const codeId of codeIds) {
            resultJsonPositions[
              this.getIdFromGraphIdAndCodeId(graphId, codeId)
            ] = { position: 0 };
          }
        }
        this.$store.commit('rj/LOAD_JSON_LOCATIONS', resultJsonPositions);
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
