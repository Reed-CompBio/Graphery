<template>
  <q-tooltip
    v-if="$store.state.settings.tooltips"
    class="text-body1"
    :self="self"
    :anchor="anchor"
    :hide-delay="hideDelay"
  >
    {{ text }}
  </q-tooltip>
</template>

<script>
  export default {
    props: {
      text: String,
      anchor: { type: String, default: 'bottom middle' },
      self: { type: String, default: 'top middle' },
      hideDelay: { type: Number, default: 0 },
    },
  };
</script>
