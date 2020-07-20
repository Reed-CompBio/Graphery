<template>
  <q-select
    dense
    label="WorkSpace"
    v-model="selectedWorkSpace"
    :options="selectOptions"
  >
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-italic text-grey">
          No WorkSpaces Exist
        </q-item-section>
      </q-item>
    </template>
  </q-select>
</template>

<script>
  import { mapState } from 'vuex';

  export default {
    data() {
      return {
        selectedWorkSpace: null,
      };
    },
    computed: {
      ...mapState('workspaces', ['tutorialSpace']),
      selectOptions() {
        if (this.tutorialSpace === null) {
          return [];
        } else {
          return this.tutorialSpace.workspaces.map((obj) => {
            return {
              label: obj.name,
              value: obj,
            };
          });
        }
      },
      currentCode() {
        return this.selectedWorkSpace.code;
      },
    },
  };
</script>
