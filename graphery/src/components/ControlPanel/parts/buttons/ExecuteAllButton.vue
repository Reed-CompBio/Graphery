<template>
  <q-btn
    flat
    icon="mdi-console-network-outline"
    @click.prevent="executeFunc"
    label="Execute All"
  ></q-btn>
</template>

<script>
  export default {
    props: ['executeFunc'],
  };
</script>
