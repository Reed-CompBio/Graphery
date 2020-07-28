<template>
  <InfoCard>
    <template v-slot:title>
      Categories
    </template>
    <q-select
      multiple
      use-chips
      v-model="categorySelection"
      :options="categoryOptions"
      emit-value
      map-options
      option-label="category"
      option-value="id"
      :loading="loadingContent"
      @change="emitValue"
    ></q-select>
  </InfoCard>
</template>

<script>
  import InfoCard from '../parts/InfoCard.vue';
  import loadingMixin from '../mixins/LoadingMixin.vue';
  import { apiCaller } from '../../../services/apis';
  import { allCategoryQuery } from '../../../services/queries';
  import { errorDialog } from '../../../services/helpers';

  export default {
    mixins: [loadingMixin],
    components: {
      InfoCard,
    },
    model: {
      prop: 'categorySelection',
      event: 'getCategorySelection',
    },
    props: {
      categorySelection: {
        type: Array,
      },
    },
    data() {
      return {
        categoryOptions: null,
      };
    },
    methods: {
      fetchValue() {
        this.startLoading();
        apiCaller(allCategoryQuery)
          .then((data) => {
            if (!data || !('allCategories' in data)) {
              throw Error('Invalid data returned.');
            }

            this.categoryOptions = data.allCategories;
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching category list. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
      emitValue() {
        this.$emit('getCategorySelection', this.categorySelection);
      },
    },
    mounted() {
      this.fetchValue();
    },
  };
</script>
