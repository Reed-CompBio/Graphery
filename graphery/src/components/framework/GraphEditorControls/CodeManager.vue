<script>
  import { mapGetters } from 'vuex';

  export default {
    computed: {
      ...mapGetters('code', [
        'getCurrentCodeId',
        'getCurrentCodeObject',
        'getCurrentCodeContent',
      ]),
      currentCodeId: {
        set(d) {
          this.$store.commit('code/LOAD_CURRENT_CODE_ID', d);
        },
        get() {
          return this.getCurrentCodeId;
        },
      },
      currentCodeObject() {
        return this.getCurrentCodeObject;
      },
    },
    methods: {
      loadCodeObjectListFromMatched(codeList) {
        this.$store.commit('code/LOAD_CODE_LIST', codeList);
      },
      updateCode(newCode) {
        this.$store.commit('code/CHANGE_CODE_CONTENT', {
          codeObject: this.currentCodeObject,
          code: newCode,
        });
        // this.afterUpdatedCode(this.currentCodeObject);
      },
      // TODO
      afterUpdatedCode(codeObj) {
        this.$store.dispatch('rj/clearResultJsonStringByCodeId', codeObj.id);
      },
    },
  };
</script>
