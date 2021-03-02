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

  export default {
    name: 'FAQ',
    components: { MarkdownSection, MaterialPage, MaterialCover },
    data() {
      return {
        faq_: `### What is Graphery?

Graphery is a platform with interactive tutorials about graph algorithms alongside real-world biological networks. It is designed with biological researchers in mind, where users can click through Python code and see _how_ the algorithms work on networks from different biological domains.

### How do I use it?

If you want a tour of the platform take the first tutorial: [Getting Started](link).  This is the best place to start!  The other tutorials are available on the [Tutorials] tab.  If you want to see the networks that are offered, click the [Graphs tab](link).  If you click a graph, you are taken to a playground view where you can interact with the graph, run the code associated with tutorials.

### How to run my own code on Graphery?

You can execute existing code in the cloud by clicking [insert cloud button] on the editor.  If you click [insert unlock button] , you will change the [user settings](link) so you can modify existing code or write your own code.  Click [insert cloud button] whenever you want the code to run.

If you would like to run your code locally on your machine (instead of in the cloud), [instructions are available here](https://docs.graphery.reedcompbio.org/user-manual/local-server/).

### I found a bug, how to report it?

Please file a [GitHub Issue](https://github.com/FlickerSoul/Graphery/issues) - thanks in advance!

### Can I make contributions to Graphery?

Yes! If you have an idea for a **graph** or a **tutorial**, then file a [GitHub Issue](https://github.com/FlickerSoul/Graphery/issues).  If you would like to add content to the website, we are always looking for contributors to add **graphs**, **tutorials**, and **translations**. [Email us to learn more](email link).

### How do I cite Graphery?

Graphery is currently under review. In the meantime, please cite our pre-print on arXiv:

Heyuan Zeng, Jinbiao Zhang, Gabriel A. Preising, Tobias Rubel, Pramesh Singh, Anna Ritz.
[_Graphery: Interactive Tutorials for Biological Network Algorithms_](https://arxiv.org/abs/2102.03469)
arXiv:2102.03469 [q-bio.MN], 2021`,
        columns: [
          {
            name: 'os',
            required: true,
            label: 'OS',
            align: 'center',
            field: 'os',
          },
          {
            name: 'version',
            align: 'center',
            label: 'OS Version',
            field: 'osVersion',
          },
          { name: 'chrome', label: 'Chrome', field: 'chrome' },
          { name: 'firefox', label: 'Firefox', field: 'firefox' },
          {
            name: 'msEdge',
            label: 'Microsoft Edge (Chromium)',
            field: 'msEdge',
          },
          { name: 'safari', label: 'Safari', field: 'safari' },
        ],
        compatibilityList: [
          {
            os: 'Linux',
            osVersion: '',
            chrome: '',
            firefox: '',
            msEdge: '',
            safari: '',
          },
          {
            os: 'MacOS',
            osVersion: '',
            chrome: '',
            firefox: '',
            msEdge: '',
            safari: '',
          },
          {
            os: 'Windows',
            osVersion: '',
            chrome: '',
            firefox: '',
            msEdge: '',
            safari: '',
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
