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
          <template>
            <q-input
              outlined
              v-model="tutorialUrl"
              hint="please input URL. Do not start or end it with -_."
            ></q-input>
          </template>
        </InfoCard>

        <InfoCard class="half-width-card">
          <template v-slot:title>
            Tutorial Name
          </template>
          <template>
            <q-input outlined v-model="tutorialName"></q-input>
          </template>
        </InfoCard>

        <InfoCard class="half-width-card">
          <template v-slot:title>
            Categories
          </template>
          <template>
            <q-select
              multiple
              use-chips
              clearable
              v-model="categoryChoices"
              :options="categoryOptions"
            ></q-select>
          </template>
        </InfoCard>

        <InfoCard class="half-width-card">
          <template v-slot:title>
            Published
          </template>
          <template>
            <q-checkbox
              v-model="tutorialPublished"
              :label="tutorialPublished ? '✅' : '❌'"
            />
          </template>
        </InfoCard>

        <q-btn class="half-width-card" label="Submit"></q-btn>
      </div>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  export default {
    props: ['url'],
    components: {
      ControlPanelContentFrame: () => import('./ControlPanelContentFrame.vue'),
      InfoCard: () => import('./InfoCard.vue'),
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
        return this.url === '-new-';
      },
    },
  };
</script>

<style lang="sass">
  .half-width-card
    width: 50%
</style>
