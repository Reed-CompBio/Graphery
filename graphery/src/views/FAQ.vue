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
        1. What is Graphery?
        <br />
        2. How do I use it?
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
  };
</script>

<style scoped></style>
