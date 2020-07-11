<template>
  <q-item>
    <q-item-section>
      <span>{{ title }}:</span>
      <span>{{ content }}</span>
    </q-item-section>
  </q-item>
</template>

<script>
  export default {
    props: ['title', 'content'],
  };
</script>
