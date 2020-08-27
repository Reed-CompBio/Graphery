<template>
  <InfoCard>
    <template v-slot:title>
      Graphs
    </template>
    <!-- TODO add a confirmation dialog during deleting tutorials -->
    <div>
      <q-select
        multiple
        use-chips
        v-model="selection"
        :options="graphOptions"
        emit-value
        map-options
        option-label="name"
        option-value="id"
        :loading="loadingContent"
      ></q-select>
    </div>
    <div class="q-mt-md">
      <q-btn label="Add All" @click="addAllGraphs" />
    </div>
  </InfoCard>
</template>

<script>
  import InfoCard from '../cards/InfoCard.vue';
  import loadingMixin from '../../mixins/LoadingMixin.vue';
  import { apiCaller } from '@/services/apis';
  import { graphSelectQuery } from '@/services/queries';
  import { errorDialog } from '@/services/helpers';

  export default {
    mixins: [loadingMixin],
    components: {
      InfoCard,
    },
    model: {
      prop: 'selectedGraphs',
      event: 'getSelectedGraphs',
    },
    props: {
      selectedGraphs: {},
    },
    data() {
      return {
        graphOptions: null,
      };
    },
    computed: {
      selection: {
        set(d) {
          this.emitValue(d);
        },
        get() {
          return this.selectedGraphs;
        },
      },
    },
    methods: {
      fetchValue() {
        this.startLoading();

        apiCaller(graphSelectQuery)
          .then((data) => {
            if (!data || !('allGraphInfo' in data)) {
              throw Error('Invalid data returned.');
            }

            this.graphOptions = data.allGraphInfo;
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
        this.$emit('getSelectedGraphs', val);
      },
      addAllGraphs() {
        this.emitValue(this.graphOptions.map((obj) => obj.id));
      },
    },
    mounted() {
      this.fetchValue();
    },
  };
</script>
