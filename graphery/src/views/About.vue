<template>
  <MaterialPage>
    <article>
      <header class="">
        <h3 class="material-page-shorter-h3">
          {{ $t('nav.About') }}
        </h3>
      </header>
      <section class="about-section">
        <p>
          Graphery is a web-based graph algorithm tutorial that is designed for
          biological researchers.
        </p>
        <p>
          It is organized around the concept of a tutorial, which describes and
          provides code for a classic graph algorithm. A tutorial contains three
          parts: text-based content, interactive graphs, and a code editor. The
          editor enables users to step forward and back in the code and see
          changes applied to the corresponding graph. The editor also allows
          more programming-savvy users to edit the existing code and see their
          modifications applied on the graphs. Users can run code in the editor
          locally or in the cloud. Together, these three panels allow users to
          gain a deeper understanding of the algorithm described.
        </p>
        <p>
          For each tutorial, users may select one of multiple real-world
          biological networks to better understand the implications of the
          algorithm described. These small graphs will come from from biological
          applications such as animal social networks, ecology food webs,
          molecular interaction networks, and phylogenetic trees.
        </p>
        <h4>
          Feedback
        </h4>
        <p>
          <a
            href="https://github.com/FlickerSoul/Graphery/issues"
            target="_blank"
            rel="noreferrer"
          >
            GitHub Issues
          </a>
        </p>
        <p>
          <a
            href="mailto:zengl@reed.edu?subject=Graphery%20Feedback&body=Please%20describe%20in%20detail%3A%0D%0A1.%20if%20something%20looks%20wrong%2C%20please%20tell%20us%20what%20it%20should%20be%20like%20and%20how%20we%20can%20reproduce%20the%20problem%0D%0A2.%20if%20something%20can%20be%20better%2C%20please%20tell%20us%20how%20we%20can%20improve%20and%20the%20reasons%0D%0A%0D%0AThank%20you%20so%20much!"
          >
            Email Me
          </a>
        </p>
        <h4>
          Contributors
        </h4>
        <ul class="uo-list">
          <li>
            Heyuan Zeng
          </li>
          <li>
            Jinbiao Zhang
          </li>
        </ul>
        <h4>
          Libraries
        </h4>
        <p>
          This website can't be done without the following open source
          libraries. Big thanks to all the contributors directly and indirectly
          making this project happen.
        </p>
        <ul class="uo-list">
          <li>
            <NewTabA link="https://quasar.dev/"> Quasar </NewTabA>
          </li>
          <li>
            <NewTabA link="https://vuejs.org">Vue.JS</NewTabA>
          </li>
          <li>
            <NewTabA link="https://github.com/hinesboy/mavonEditor">
              Mavon Editor
            </NewTabA>
          </li>
          <li>
            <NewTabA link="https://github.com/markdown-it/markdown-it">
              Markdown It
            </NewTabA>
          </li>
          <li>
            <NewTabA
              link="https://github.com/markdown-it/markdown-it#syntax-extensions"
            >
              Markdown It Extensions
            </NewTabA>
          </li>
          <li>
            <NewTabA link="https://github.com/cytoscape/cytoscape.js">
              Cytoscape.JS
            </NewTabA>
          </li>
          <li>
            <NewTabA link="https://js.cytoscape.org/#extensions">
              Cytoscape.JS Extensions
            </NewTabA>
          </li>
          <li>
            <NewTabA link="https://github.com/atomiks/tippyjs">
              Tippy.JS
            </NewTabA>
          </li>
          <li>
            <NewTabA link="https://github.com/Microsoft/monaco-editor">
              Monaco Editor
            </NewTabA>
          </li>
          <li>
            <NewTabA link="https://github.com/cool-RR/PySnooper">
              PySnooper
            </NewTabA>
          </li>
          <li>
            <NewTabA link="https://www.djangoproject.com/"> Django </NewTabA>
          </li>
          <li>
            <NewTabA link="https://github.com/graphql-python/graphene-django">
              Graphene Django
            </NewTabA>
          </li>
          <li>
            <NewTabA link="https://www.postgresql.org/"> PostgreSQL </NewTabA>
          </li>
        </ul>
        <LicenseCard></LicenseCard>
      </section>
    </article>
  </MaterialPage>
</template>

<script>
  import NewTabA from '../components/framework/NewTabA';
  export default {
    components: {
      NewTabA,
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
      LicenseCard: () => import('@/components/framework/LicenseCard.vue'),
    },
  };
</script>

<style lang="sass">
  .about-section
    p
      font-size: 1.2rem
  .uo-list
    font-size: 1.1rem
</style>
