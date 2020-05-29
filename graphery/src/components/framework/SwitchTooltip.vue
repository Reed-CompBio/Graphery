<template>
  <q-tooltip v-if="$store.state.settings.tooltips" class="text-body1">
    {{ text }}
  </q-tooltip>
</template>

<script>
  export default {
    props: ['text'],
  };
</script>
