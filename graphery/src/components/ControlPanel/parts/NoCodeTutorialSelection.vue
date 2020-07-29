<template>
  <InfoCard>
    <template v-slot:title>
      Tutorial
    </template>
    <!-- TODO add a confirmation dialog during deleting tutorials -->
    <q-select
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
  import { allTutorialNoCodeQuery } from '../../../services/queries';
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
      currentTutorial: {
        type: String,
        default: null,
      },
      selectedTutorial: {
        type: String,
      },
    },
    data() {
      return {
        tutorialOptions: null,
      };
    },
    methods: {
      fetchValue() {
        this.startLoading();

        apiCaller(allTutorialNoCodeQuery, {
          currentTutorial: this.currentTutorial,
        })
          .then((data) => {
            if (!data || !('allTutorialInfoNoCode' in data)) {
              throw Error('Invalid data returned.');
            }

            this.tutorialOptions = data.allTutorialInfoNoCode;
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
