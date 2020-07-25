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
        <LicenseCard></LicenseCard>
      </section>
    </article>
  </MaterialPage>
</template>

<script>
  export default {
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
      LicenseCard: () => import('@/components/framework/LicenseCard.vue'),
    },
  };
</script>

<style lang="sass">
  .about-section
    p
      font-size: 1.2rem
</style>
