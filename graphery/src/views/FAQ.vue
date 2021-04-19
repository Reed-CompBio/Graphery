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
        <q-separator />
        <div>
          <q-table
            :title="$t('Browser Compatibility')"
            :columns="columns"
            :data="compatibilityList"
            row-key="os"
          >
          </q-table>
        </div>
      </section>
    </MaterialPage>
  </div>
</template>

<script>
  import MaterialCover from '@/components/framework/MaterialCover';
  import MaterialPage from '@/components/framework/MaterialPage';
  import MarkdownSection from '@/components/framework/md/MarkdownSection';

  import faqEnUs from '@/components/static/faq_en_us.md';

  export default {
    name: 'FAQ',
    components: { MarkdownSection, MaterialPage, MaterialCover },
    data() {
      return {
        faq_: faqEnUs,
        columns: [
          {
            name: 'os',
            required: true,
            label: 'OS',
            align: 'center',
            field: 'os',
          },
          { name: 'chrome', label: 'Chrome', field: 'chrome', align: 'center' },
          {
            name: 'firefox',
            label: 'Firefox',
            field: 'firefox',
            align: 'center',
          },
          {
            name: 'msEdge',
            label: 'Microsoft Edge (Chromium)',
            field: 'msEdge',
            align: 'center',
          },
          { name: 'safari', label: 'Safari', field: 'safari', align: 'center' },
        ],
        compatibilityList: [
          {
            os: 'Linux',
            chrome: 'last 10 Chrome versions',
            firefox: 'last 10 Firefox versions',
            msEdge: 'last 4 Edge versions',
            safari: 'N/A',
          },
          {
            os: 'MacOS',
            chrome: 'last 10 Chrome versions',
            firefox: 'last 10 Firefox versions',
            msEdge: 'last 4 Edge versions',
            safari: 'last 7 Safari versions',
          },
          {
            os: 'Windows',
            chrome: 'last 10 Chrome versions',
            firefox: 'last 10 Firefox versions',
            msEdge: 'last 4 Edge versions',
            safari: 'N/A',
          },
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
