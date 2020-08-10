<template>
  <q-btn label="Submit" @click="action" :loading="loading" />
</template>

<script>
  export default {
    props: ['action', 'loading'],
  };
</script>
