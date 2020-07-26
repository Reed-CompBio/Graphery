<template>
  <q-btn :label="label" @click="action" :to="routePath" flat>
    <SwitchTooltip text="Open In Editor"></SwitchTooltip>
  </q-btn>
</template>

<script>
  import SwitchTooltip from '../../framework/SwitchTooltip.vue';

  export default {
    props: {
      label: {
        default: '',
      },
      action: {
        default: () => () => null,
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
