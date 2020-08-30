<template>
  <InfoCard>
    <template v-slot:title>
      Tutorials
    </template>
    <!-- TODO add a confirmation dialog during deleting tutorials -->
    <div>
      <q-select
        :multiple="multipleSelection"
        :use-chips="multipleSelection"
        v-model="selection"
        :options="tutorialOptions"
        clearable
        emit-value
        map-options
        option-label="name"
        option-value="id"
        :loading="loadingContent"
      ></q-select>
    </div>
    <div v-if="multipleSelection" class="q-mt-md">
      <q-btn label="Add All" @click="addAll" />
    </div>
  </InfoCard>
</template>

<script>
  import InfoCard from '../cards/InfoCard.vue';
  import loadingMixin from '../../mixins/LoadingMixin.vue';
  import { apiCaller } from '@/services/apis';
  import { tutorialSelectQuery } from '@/services/queries';
  import { errorDialog } from '@/services/helpers';

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
      multipleSelection: {
        type: Boolean,
        default: true,
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
      addAll() {
        this.emitValue(this.tutorialOptions.map((obj) => obj.id));
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
