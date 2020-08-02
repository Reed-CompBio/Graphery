<template>
  <InfoCard>
    <template v-slot:title>
      Authors
    </template>
    <q-select
      multiple
      use-chips
      v-model="selection"
      :options="authorOptions"
      emit-value
      map-options
      option-label="username"
      option-value="id"
      :loading="loadingContent"
    ></q-select>
  </InfoCard>
</template>

<script>
  import InfoCard from '../parts/InfoCard.vue';
  import loadingMixin from '../mixins/LoadingMixin.vue';
  import { apiCaller } from '../../../services/apis';
  import { authorSelectQuery } from '../../../services/queries';
  import { errorDialog } from '../../../services/helpers';

  export default {
    mixins: [loadingMixin],
    components: {
      InfoCard,
    },
    model: {
      prop: 'authorSelection',
      event: 'getAuthorSelection',
    },
    props: {
      authorSelection: {
        type: Array,
      },
    },
    data() {
      return {
        authorOptions: null,
      };
    },
    computed: {
      selection: {
        set(d) {
          this.emitValue(d);
        },
        get() {
          return this.authorSelection;
        },
      },
    },
    methods: {
      fetchValue() {
        this.startLoading();

        apiCaller(authorSelectQuery)
          .then((data) => {
            if (!data || !('allAuthors' in data)) {
              throw Error('Invalid data returned.');
            }

            this.authorOptions = data.allAuthors;
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching author list. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
      emitValue(val) {
        this.$emit('getAuthorSelection', val);
      },
    },
    mounted() {
      this.fetchValue();
    },
  };
</script>
