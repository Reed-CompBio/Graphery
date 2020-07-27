<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Category Editor
    </template>
    <template>
      <div style="display: flex; flex-direction: column;" class="flex-center">
        <InfoCard class="half-width-card q-mb-md">
          <template v-slot:title>
            ID
          </template>
          <div class="text-center">
            {{ displayedId }}
          </div>
        </InfoCard>
        <InfoCard class="half-width-card">
          <template v-slot:title>
            Category
          </template>
          <q-input
            outlined
            v-model="category"
            hint="Please input the name of this category."
          />
        </InfoCard>
        <InfoCard class="half-width-card">
          <template v-slot:title>
            Published?
          </template>
          <q-checkbox
            v-model="categoryPublished"
            :label="categoryPublished ? '✅' : '❌'"
          />
        </InfoCard>

        <SubmitButton class="half-width-card" :action="postValue" />
      </div>
      <q-inner-loading :showing="loadingContent">
        <q-spinner-pie size="64px" color="primary" />
      </q-inner-loading>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin.vue';
  import { newModelUUID } from '../../../services/params';
  import { apiCaller } from '../../../services/apis';
  import {
    categoryQuery,
    updateCategoryMutation,
  } from '../../../services/queries';
  import { errorDialog, successDialog } from '../../../services/helpers';
  import SubmitButton from '../parts/SubmitButton';

  export default {
    mixins: [loadingMixin],
    props: {
      id: {
        default: newModelUUID,
      },
    },
    components: {
      SubmitButton,
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        category: '',
        categoryPublished: false,
      };
    },
    computed: {
      newCategory() {
        return this.id === newModelUUID;
      },
      displayedId() {
        if (this.newCategory) {
          return 'Pending';
        } else {
          return this.id;
        }
      },
    },
    methods: {
      fetchValue() {
        if (!this.newCategory) {
          this.startLoading();

          apiCaller(categoryQuery, {
            id: this.id,
          })
            .then((data) => {
              if (!data || !('category' in data) || !data.category) {
                throw Error(
                  'Invalid data returned. Cannot modify current entry.'
                );
              }

              this.category = data.category.category;
              this.categoryPublished = data.category.isPublished;
            })
            .catch((err) => {
              errorDialog({
                message: `An error occurs during fetching Category. ${err}`,
              });
            })
            .finally(() => {
              this.finishedLoading();
            });
        }
      },
      pushToNewPlace(id) {
        if (this.newCategory) {
          this.$router.push({ name: 'Category Editor', params: { id } });
        }
      },
      postValue() {
        this.startLoading();
        apiCaller(updateCategoryMutation, {
          id: this.id,
          category: this.category,
          isPublished: this.categoryPublished,
        })
          .then((data) => {
            if (!data || !('updateCategory' in data)) {
              throw Error('Invalid data returned.');
            }

            if (!data.updateCategory.success) {
              throw Error('Cannot modify category for unknown reason');
            }

            this.pushToNewPlace(data.updateCategory.id);
            successDialog({
              message: 'Update Category Successfully!',
            });
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during updating category entry. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
            this.fetchValue();
          });
      },
    },
    beforeMount() {
      this.fetchValue();
    },
  };
</script>
