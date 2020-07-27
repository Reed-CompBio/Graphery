<template>
  <q-btn
    flat
    icon="mdi-card-plus-outline"
    @click.prevent="createFunc"
    label="Add New"
  ></q-btn>
</template>

<script>
  export default {
    props: ['createFunc'],
  };
</script>
