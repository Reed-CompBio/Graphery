<template>
  <InfoCard>
    <template v-slot:title>
      Add Graphs
    </template>
    <!-- TODO add a confirmation dialog during deleting tutorials -->
    <q-select
      multiple
      use-chips
      v-model="selection"
      :options="graphOptions"
      map-options
      option-label="name"
      :loading="loadingContent"
    ></q-select>
  </InfoCard>
</template>

<script>
  import InfoCard from '../parts/InfoCard.vue';
  import loadingMixin from '../mixins/LoadingMixin.vue';
  import { apiCaller } from '../../../services/apis';
  import { tutorialSelectQuery } from '../../../services/queries';
  import { errorDialog } from '../../../services/helpers';

  export default {
    mixins: [loadingMixin],
    components: {
      InfoCard,
    },
    model: {
      prop: 'selectedTutorial',
      event: 'getSelectedTutorial',
    },
    props: {
      singleSelection: {
        type: Boolean,
        default: false,
      },
      selectedTutorial: {},
    },
    data() {
      return {
        tutorialOptions: null,
      };
    },
    methods: {
      fetchValue() {
        this.startLoading();

        apiCaller(tutorialSelectQuery)
          .then((data) => {
            if (!data || !('allTutorialInfo' in data)) {
              throw Error('Invalid data returned.');
            }

            this.tutorialOptions = data.allTutorialInfo;
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching tutorial list. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
      emitValue(val) {
        this.$emit('getSelectedTutorial', val);
      },
    },
    computed: {
      selection: {
        set(d) {
          this.emitValue(d);
        },
        get() {
          return this.selectedTutorial;
        },
      },
    },
    mounted() {
      this.fetchValue();
    },
  };
</script>
