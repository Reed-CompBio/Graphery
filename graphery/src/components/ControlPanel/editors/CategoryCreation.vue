<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Category Editor
    </template>
    <template>
      <div style="display: flex; flex-direction: column;" class="flex-center">
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

        <q-btn class="half-width-card" label="Submit" />
      </div>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { newContentTag } from '../../../services/params';

  export default {
    props: ['id'],
    components: {
      ControlPanelContentFrame: () => import('../ControlPanelContentFrame.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        category: '',
      };
    },
    computed: {
      newCategory() {
        return this.id === newContentTag;
      },
    },
  };
</script>
