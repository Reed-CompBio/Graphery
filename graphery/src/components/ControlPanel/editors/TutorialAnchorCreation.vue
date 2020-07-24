<template>
  <ControlPanelContentFrame>
    <template slot="title">
      Tutorial Anchor Editor
    </template>
    <template>
      <div style="display: flex; flex-direction: column;" class="flex-center">
        <InfoCard class="half-width-card">
          <template v-slot:title>
            Tutorial URL
          </template>
          <q-input
            outlined
            v-model="tutorialUrl"
            hint="Please input URL. Do not start or end it with -_."
          />
        </InfoCard>

        <InfoCard class="half-width-card">
          <template v-slot:title>
            Tutorial Name
          </template>
          <q-input outlined v-model="tutorialName"></q-input>
        </InfoCard>

        <InfoCard class="half-width-card">
          <template v-slot:title>
            Categories
          </template>
          <q-select
            multiple
            use-chips
            clearable
            v-model="categoryChoices"
            :options="categoryOptions"
          ></q-select>
        </InfoCard>

        <InfoCard class="half-width-card">
          <template v-slot:title>
            Published
          </template>
          <q-checkbox
            v-model="tutorialPublished"
            :label="tutorialPublished ? '✅' : '❌'"
          />
        </InfoCard>

        <q-btn class="half-width-card" label="Submit" />
      </div>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { newContentTag } from '../../../services/params';

  export default {
    props: ['url'],
    components: {
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        tutorialUrl: '',
        tutorialName: '',
        categoryChoices: [],
        categoryOptions: [],
        tutorialPublished: false,
      };
    },
    computed: {
      isCreatingNewAnchor() {
        return this.url === newContentTag;
      },
    },
  };
</script>

<style lang="sass">
  .half-width-card
    width: 50%
</style>
