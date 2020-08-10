<template>
  <q-btn :label="label" :to="routePath" flat style="text-transform: none; ">
    <SwitchTooltip text="Open In Editor"></SwitchTooltip>
  </q-btn>
</template>

<script>
  import SwitchTooltip from '../../../framework/SwitchTooltip.vue';

  export default {
    props: {
      label: {
        default: '',
      },
      routePath: {
        default: null,
      },
    },
    components: {
      SwitchTooltip,
    },
  };
</script>
