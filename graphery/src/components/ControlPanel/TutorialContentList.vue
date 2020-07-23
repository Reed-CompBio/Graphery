<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Tutorial Contents
    </template>
    <template>
      <q-table></q-table>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  export default {
    components: {
      ControlPanelContentFrame: () => import('./ControlPanelContentFrame'),
    },
    data() {
      return {
        columns: [],
      };
    },
  };
</script>
