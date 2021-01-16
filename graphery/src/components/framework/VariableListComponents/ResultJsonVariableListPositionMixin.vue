<script>
  import { mapGetters } from 'vuex';

  export default {
    computed: {
      ...mapGetters('code', ['getCurrentCodeId']),
      ...mapGetters('graphs', ['getCurrentGraphId']),
      ...mapGetters('rj', ['getToggleState']),
      currentPositionId() {
        return this.getIdFromGraphIdAndCodeId(
          this.getCurrentGraphId,
          this.getCurrentCodeId
        );
      },
    },
    methods: {
      getIdFromGraphIdAndCodeId(graphId, codeId) {
        return `${graphId}-${codeId}`;
      },
      updateVariableToggleState(varIdentifier, toggleState) {
        this.$store.commit('rj/UPDATE_VARIABLE_LIST_TOGGLE_STATE', {
          positionId: this.currentPositionId,
          identifier: varIdentifier,
          toggleState: toggleState,
        });
      },
    },
  };
</script>
