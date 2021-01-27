<template>
  <div>
    <MaterialCover :cover-title="$t('nav.tos')" />
    <MaterialPage>
      <header>
        <h3 class="material-page-shorter-h3">{{ $t('nav.tos') }} (TOS)</h3>
        <q-separator />
      </header>
    </MaterialPage>
  </div>
</template>

<script>
  import MaterialCover from '@/components/framework/MaterialCover';
  import MaterialPage from '@/components/framework/MaterialPage';
  export default {
    name: 'TOS',
    components: { MaterialPage, MaterialCover },
  };
</script>

<style scoped></style>
