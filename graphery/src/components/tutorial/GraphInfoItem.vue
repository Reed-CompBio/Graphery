<template>
  <q-item>
    <q-item-section>
      <span>{{ title }}:</span>
      <div v-if="!!html" v-html="html"></div>
      <span v-else>{{ content }}</span>
    </q-item-section>
  </q-item>
</template>

<script>
  export default {
    props: ['title', 'content', 'html'],
  };
</script>
