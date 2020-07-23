<template>
  <q-btn flat icon="refresh" @click.prevent="fetchFunc" label="Refresh"></q-btn>
</template>

<script>
  export default {
    props: ['fetchFunc'],
  };
</script>
