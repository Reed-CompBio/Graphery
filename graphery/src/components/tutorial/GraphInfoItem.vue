<template>
  <q-item>
    <q-item-section>
      <span>{{ title }}:</span>
      <div v-if="!!html">
        <MarkdownSection :input-html="html" />
      </div>
      <span v-else>{{ content }}</span>
    </q-item-section>
  </q-item>
</template>

<script>
  export default {
    components: {
      MarkdownSection: () =>
        import('@/components/framework/md/MarkdownSection'),
    },
    props: ['title', 'content', 'html'],
  };
</script>
