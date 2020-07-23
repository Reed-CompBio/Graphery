<template>
  <q-btn :label="label" @click.prevent="action" :to="routePath" flat>
    <SwitchTooltip text="Open In Editor"></SwitchTooltip>
  </q-btn>
</template>

<script>
  import SwitchTooltip from '../../framework/SwitchTooltip.vue';

  export default {
    props: ['label', 'action', 'routePath'],
    components: {
      SwitchTooltip,
    },
  };
</script>
