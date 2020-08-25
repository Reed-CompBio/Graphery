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

        <RankSelection
          class="half-width-card"
          v-model="tutorialAnchorObj.rank"
        />

        <CategorySelection
          v-model="tutorialAnchorObj.categories"
          class="half-width-card"
        />

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
  import { newModelUUID } from '@/services/params';
  import { apiCaller } from '@/services/apis';
  import loadingMixin from '../mixins/LoadingMixin';
  import pushToMixin from '../mixins/PushToMixin.vue';
  import leaveConfirmMixin from '../mixins/LeaveConfirmMixin.vue';
  import {
    tutorialQuery,
    updateTutorialAnchorMutation,
  } from '@/services/queries';
  import { errorDialog, successDialog } from '@/services/helpers';
  import CategorySelection from '../parts/selectors/CategorySelection';

  export default {
    mixins: [loadingMixin, pushToMixin, leaveConfirmMixin],
    props: ['id'],
    components: {
      CategorySelection,
      RankSelection: () =>
        import('@/components/ControlPanel/parts/selectors/RankSelection'),
      IDCard: () => import('../parts/cards/IDCard'),
      SubmitButton: () => import('../parts/buttons/SubmitButton'),
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      InfoCard: () => import('../parts/cards/InfoCard.vue'),
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

            this.tutorialAnchorObj.id = data.updateTutorialAnchor.model.id;
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
