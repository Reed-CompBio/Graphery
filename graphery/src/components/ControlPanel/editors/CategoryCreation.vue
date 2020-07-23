<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Category Editor
    </template>
    <template> </template>
  </ControlPanelContentFrame>
</template>

<script>
  export default {
    components: {
      ControlPanelContentFrame: () => import('../ControlPanelContentFrame.vue'),
    },
  };
</script>
