<template>
  <ControlPanelContentFrame>
    <template slot="title">
      Tutorial Anchor Editor
    </template>
    <template>
      <div style="display: flex; flex-direction: column;" class="flex-center">
        <IDCard class="half-width-card" :id="this.tutorialAnchorObj.id" />
        <InfoCard class="half-width-card">
          <template v-slot:title>
            Tutorial URL
          </template>
          <q-input
            outlined
            v-model="tutorialAnchorObj.url"
            hint="Please input URL. Do not start or end it with -_."
          />
        </InfoCard>

        <InfoCard class="half-width-card">
          <template v-slot:title>
            Tutorial Name
          </template>
          <q-input outlined v-model="tutorialAnchorObj.name"></q-input>
        </InfoCard>

        <InfoCard class="half-width-card">
          <template v-slot:title>
            Categories
          </template>
          <q-select
            multiple
            use-chips
            v-model="tutorialAnchorObj.categories"
            :options="categoryOptions"
            :loading="loadingCategory"
            emit-value
            map-options
            option-label="category"
            option-value="id"
          ></q-select>
        </InfoCard>

        <InfoCard class="half-width-card">
          <template v-slot:title>
            Published
          </template>
          <q-checkbox
            v-model="tutorialAnchorObj.isPublished"
            :label="tutorialAnchorObj.isPublished ? '✅' : '❌'"
          />
        </InfoCard>

        <SubmitButton :loading="loadingContent" :action="postTutorial" />
      </div>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { newModelUUID } from '../../../services/params';
  import { apiCaller } from '../../../services/apis';
  import loadingMixin from '../mixins/LoadingMixin';
  import pushToMixin from '../mixins/PushToMixin.vue';
  import {
    allCategoryQuery,
    tutorialQuery,
    updateTutorialAnchorMutation,
  } from '../../../services/queries';
  import { errorDialog, successDialog } from '../../../services/helpers';
  import SubmitButton from '../parts/SubmitButton';
  import IDCard from '../parts/IDCard';

  export default {
    mixins: [loadingMixin, pushToMixin],
    props: ['id'],
    components: {
      IDCard,
      SubmitButton,
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        tutorialAnchorObj: {
          id: this.id,
          url: '',
          name: '',
          categories: [],
          isPublished: false,
        },
        categoryOptions: [],
        loadingCategory: false,
      };
    },
    computed: {
      isCreatingNew() {
        return this.tutorialAnchorObj.id === newModelUUID;
      },
    },
    methods: {
      fetchValue() {
        if (!this.isCreatingNew) {
          this.startLoading();
          apiCaller(tutorialQuery, { id: this.tutorialAnchorObj.id })
            .then((data) => {
              if (!data || !('tutorial' in data)) {
                throw Error('Invalid data returned.');
              }

              this.tutorialAnchorObj = {
                ...this.tutorialAnchorObj,
                ...data.tutorial,
                categories: data.tutorial.categories.map((obj) => obj.id),
              };
            })
            .catch((err) => {
              errorDialog({
                message: `An error occurs during fetching tutorial anchor detail. ${err}`,
              });
            })
            .finally(() => {
              this.finishedLoading();
            });
        }

        this.loadingCategory = true;
        apiCaller(allCategoryQuery)
          .then((data) => {
            if (!data || !('allCategories' in data)) {
              throw Error('Invalid data returned.');
            }

            this.categoryOptions = data.allCategories;
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching all categories. ${err}`,
            });
          })
          .then(() => {
            this.loadingCategory = false;
          });
      },
      postTutorial() {
        this.startLoading();
        apiCaller(updateTutorialAnchorMutation, this.tutorialAnchorObj)
          .then((data) => {
            if (!data || !('updateTutorialAnchor' in data)) {
              throw Error('Invalid data returned.');
            }

            if (!data.updateTutorialAnchor.success) {
              throw Error('Cannot update tutorial anchor at this time.');
            }

            this.pushToNewPlace(this.tutorialAnchorObj.id);
            successDialog({
              message: 'Update Tutorial Anchor Successfully!',
            });
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching tutorial anchor detail. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
    },
    mounted() {
      this.fetchValue();
    },
  };
</script>

<style lang="sass">
  .half-width-card
    width: 50%
</style>
