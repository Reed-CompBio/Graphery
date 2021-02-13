<template>
  <div>
    <MaterialCover :cover-title="$t('nav.faq')" />
    <MaterialPage>
      <header>
        <h3 class="material-page-shorter-h3">{{ $t('nav.faq') }} (FAQ)</h3>
        <q-separator />
      </header>
      <section>
        <div class="q-my-lg q-pa-sm">
          <MarkdownSection :markdown-raw="faq" />
        </div>
      </section>
    </MaterialPage>
  </div>
</template>

<script>
  import MaterialCover from '@/components/framework/MaterialCover';
  import MaterialPage from '@/components/framework/MaterialPage';
  import MarkdownSection from '@/components/framework/md/MarkdownSection';
  export default {
    name: 'FAQ',
    components: { MarkdownSection, MaterialPage, MaterialCover },
    data() {
      return {
        faq_: `
### What is Graphery?

Coming Soon

### How do I use it?

Coming Soon

### How to run my own code on Graphery?

Coming Soon

### I found a bug, how to report it?

Coming Soon

### Can I make contributions to Graphery?

Coming Soon

`,
        examples: [
          'What is Graphery?',
          'How do I use it?',
          'How to run my own code on Graphery?',
          'I found a bug, how to report it?',
          'Can I make contributions to Graphery?',
        ],
      };
    },
    computed: {
      faq() {
        return this.faq_;
      },
    },
  };
</script>

<style lang="sass" scoped></style>
