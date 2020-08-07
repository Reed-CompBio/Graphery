<template>
  <q-btn
    :label="label"
    :to="routePath"
    flat
    :disable="disabled"
    style="text-transform: none;"
  >
    <SwitchTooltip text="Open Page"></SwitchTooltip>
  </q-btn>
</template>
<script>
  import SwitchTooltip from '../../framework/SwitchTooltip.vue';
  export default {
    props: ['label', 'routePath', 'disabled'],
    components: { SwitchTooltip },
  };
</script>
