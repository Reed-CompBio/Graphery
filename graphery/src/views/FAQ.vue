<template>
  <div>
    <MaterialCover :cover-title="$t('nav.faq')" />
    <MaterialPage>
      <header>
        <h3 class="material-page-shorter-h3">
          {{ $t('nav.faq') }}
        </h3>
        <q-separator />
      </header>
      <body>
        <!-- example questions -->
        <p v-for="(item, index) in examples" :key="index">
          {{ index + 1 }}.
          {{ item }}
        </p>
      </body>
    </MaterialPage>
  </div>
</template>

<script>
  import MaterialCover from '@/components/framework/MaterialCover';
  import MaterialPage from '@/components/framework/MaterialPage';
  export default {
    name: 'FAQ',
    components: { MaterialPage, MaterialCover },
    data() {
      return {
        examples: [
          'What is Graphery?',
          'How do I use it?',
          'How to run my own code on Graphery?',
          'I found a bug, how to report it?',
          'Can I make contributions to Graphery?',
        ],
      };
    },
  };
</script>

<style scoped></style>
