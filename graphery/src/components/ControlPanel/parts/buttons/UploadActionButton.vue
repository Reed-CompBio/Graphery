<template>
  <q-btn flat :label="label" @click="$emit('click')" :color="color" />
</template>

<script>
  export default {
    props: {
      label: {
        type: String,
      },
      color: {
        default: 'black',
      },
    },
  };
</script>
