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
  export default {
    name: 'TOS',
    components: { MarkdownSection, MaterialPage, MaterialCover },
    data() {
      return {
        tosContent_: `By continuing to access Graphery, you agree to the terms of service and privacy notice.

The Graphery service is provided for free on an as-is basis. Use this service at your own risk. Do not use it to share confidential information. The developers of Graphery are not responsible for the actions of any of the users on this website. We are also not responsible for any damages caused by using this website. Finally, it is your responsibility to follow appropriate academic integrity standards. All articles(tutorials, graphs, etc.) without special specification are licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)

![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)

### Privacy Policy

By using [Graphery](https://graphery.reedcompbio.org), your visualized code, options, user interactions, and IP address are logged on our server and your activities (viewed pages, viewport movements, and click events) by Google Analytics. Nearly all web services collect this basic information from users in their server logs. However, Graphery does not collect any personally identifiable information from its users.
`,
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
