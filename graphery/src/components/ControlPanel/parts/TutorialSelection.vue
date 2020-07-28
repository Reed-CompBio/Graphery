<template>
  <InfoCard>
    <template v-slot:title>
      Tutorials
    </template>
    <!-- TODO add a confirmation dialog during deleting tutorials -->
    <q-select
      :multiple="!singleSelection"
      :use-chips="!singleSelection"
      v-model="selection"
      :options="tutorialOptions"
      emit-value
      map-options
      option-label="name"
      option-value="id"
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
        selection: this.selectedTutorial,
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
      emitValue() {
        this.$emit('getSelectedTutorial', this.selection);
      },
    },
    watch: {
      selectedTutorial: function() {
        this.emitValue();
      },
    },
    mounted() {
      this.fetchValue();
    },
  };
</script>
