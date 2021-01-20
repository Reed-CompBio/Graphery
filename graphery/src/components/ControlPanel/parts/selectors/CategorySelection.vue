<template>
  <InfoCard>
    <template v-slot:title>
      <span class="text">{{ $t('collectionPage.Filter') }}</span>
    </template>
    <q-select
      multiple
      use-chips
      v-model="selection"
      :options="categoryOptions"
      emit-value
      map-options
      option-label="category"
      option-value="id"
      :label="labelName"
      :loading="loadingContent"
    >
      <template v-slot:no-option>
        <q-item>
          <q-item-section class="text-grey">
            No Items
          </q-item-section>
        </q-item>
      </template>
    </q-select>
  </InfoCard>
</template>

<script>
  import loadingMixin from '../../mixins/LoadingMixin.vue';
  import { apiCaller } from '@/services/apis';
  import { allCategoryQuery } from '@/services/queries';
  import { errorDialog } from '@/services/helpers';

  export default {
    mixins: [loadingMixin],
    components: {
      InfoCard: () => import('../cards/InfoCard.vue'),
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
      emitValue(val) {
        this.$emit('getCategorySelection', val);
      },
    },
    computed: {
      selection: {
        set(d) {
          this.emitValue(d);
        },
        get() {
          return this.categorySelection;
        },
      },
      labelName() {
        return this.$t('collectionPage.Categories');
      },
    },
    mounted() {
      this.fetchValue();
    },
  };
</script>
