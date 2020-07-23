<template>
  <q-btn :label="label" @click.prevent="acton" :to="routePath" flat>
    <SwitchTooltip text="Open Page"></SwitchTooltip>
  </q-btn>
</template>
<script>
  import SwitchTooltip from '../../framework/SwitchTooltip.vue';
  export default {
    props: ['label', 'acton', 'routePath'],
    components: { SwitchTooltip },
  };
</script>
