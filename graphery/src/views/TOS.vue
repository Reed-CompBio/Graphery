<template>
  <div>
    <MaterialCover :cover-title="$t('nav.tos')" />
    <MaterialPage>
      <header>
        <h3 class="material-page-shorter-h3">
          {{ $t('nav.tos') }} (TOS) and Privacy Notce
        </h3>
        <!-- TODO i18n -->
        <q-separator />
      </header>
      <section>
        <div class="q-my-lg q-pa-sm ">
          <MarkdownSection :markdown-raw="tosContent" />
        </div>
      </section>
    </MaterialPage>
  </div>
</template>

<script>
  import MaterialCover from '@/components/framework/MaterialCover';
  import MaterialPage from '@/components/framework/MaterialPage';
  import MarkdownSection from '@/components/framework/md/MarkdownSection';

  import tosEnUs from '@/components/static/tos_en_us.md';

  export default {
    name: 'TOS',
    components: { MarkdownSection, MaterialPage, MaterialCover },
    data() {
      return {
        tosContent_: tosEnUs,
      };
    },
    computed: {
      tosContent() {
        return this.tosContent_;
      },
    },
  };
</script>

<style scoped></style>
