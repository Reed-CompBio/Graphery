<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Category Editor
    </template>
    <template>
      <div style="display: flex; flex-direction: column;" class="flex-center">
        <IDCard class="half-width-card q-mb-md" :id="this.categoryObj.id" />
        <InfoCard class="half-width-card">
          <template v-slot:title>
            Category
          </template>
          <q-input
            outlined
            v-model="categoryObj.category"
            hint="Please input the name of this category."
          />
        </InfoCard>
        <InfoCard class="half-width-card">
          <template v-slot:title>
            Published?
          </template>
          <q-checkbox
            v-model="categoryObj.isPublished"
            :label="categoryObj.isPublished ? '✅' : '❌'"
          />
        </InfoCard>

        <SubmitButton
          class="half-width-card"
          :loading="loadingContent"
          :action="postValue"
        />
      </div>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin.vue';
  import pushToMixin from '../mixins/PushToMixin.vue';
  import { newModelUUID } from '../../../services/params';
  import { apiCaller } from '../../../services/apis';
  import {
    categoryQuery,
    updateCategoryMutation,
  } from '../../../services/queries';
  import { errorDialog, successDialog } from '../../../services/helpers';
  import SubmitButton from '../parts/SubmitButton';
  import IDCard from '../parts/IDCard';

  export default {
    mixins: [loadingMixin, pushToMixin],
    props: {
      id: {
        default: newModelUUID,
      },
    },
    components: {
      IDCard,
      SubmitButton,
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        categoryObj: {
          id: this.id,
          category: '',
          isPublished: false,
        },
      };
    },
    computed: {
      isCreatingNew() {
        return this.id === newModelUUID;
      },
    },
    methods: {
      fetchValue() {
        if (!this.isCreatingNew) {
          this.startLoading();

          apiCaller(categoryQuery, {
            id: this.categoryObj.id,
          })
            .then((data) => {
              if (!data || !('category' in data) || !data.category) {
                throw Error(
                  'Invalid data returned. Cannot modify current entry.'
                );
              }

              this.categoryObj = data.category;
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
      postValue() {
        this.startLoading();
        apiCaller(updateCategoryMutation, this.categoryObj)
          .then((data) => {
            if (!data || !('updateCategory' in data)) {
              throw Error('Invalid data returned.');
            }

            if (!data.updateCategory.success) {
              throw Error('Cannot modify category for unknown reason');
            }

            this.categoryObj = data.updateCategory.model;
            this.pushToNewPlace(this.categoryObj.id);

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
          });
      },
    },
    beforeMount() {
      this.fetchValue();
    },
  };
</script>
