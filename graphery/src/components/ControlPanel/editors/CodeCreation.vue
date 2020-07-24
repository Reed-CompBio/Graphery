<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Code Editor
    </template>
    <template> </template>
  </ControlPanelContentFrame>
</template>

<script>
  export default {
    components: {
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
    },
  };
</script>
