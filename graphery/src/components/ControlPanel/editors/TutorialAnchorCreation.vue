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
            clearable
            v-model="tutorialAnchorObj.categories"
            :options="categoryOptions"
            :loading="loadingCategory"
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
  import {
    allCategoryQuery,
    tutorialQuery,
    updateTutorialAnchorMutation,
  } from '../../../services/queries';
  import { errorDialog, successDialog } from '../../../services/helpers';
  import SubmitButton from '../parts/SubmitButton';
  import IDCard from '../parts/IDCard';

  export default {
    mixins: [loadingMixin],
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
      isCreatingNewAnchor() {
        return this.tutorialAnchorObj.id === newModelUUID;
      },
    },
    methods: {
      fetchValue() {
        if (!this.isCreatingNewAnchor) {
          this.startLoading();
          apiCaller(tutorialQuery, { id: this.tutorialAnchorObj.id })
            .then((data) => {
              if (!data || !('tutorial' in data)) {
                throw Error('Invalid data returned.');
              }

              this.tutorialAnchorObj = {
                ...this.tutorialAnchorObj,
                ...data.tutorial,
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

            this.categoryOptions = data.allCategories.map(
              (obj) => obj.category
            );
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
      pushToNewPlace(id) {
        if (this.url === newModelUUID) {
          this.$router.push({
            name: 'Tutorial Anchor Editor',
            params: { id },
          });
        }
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

            this.pushToNewPlace(this.tutorialAnchorObj.url);
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
