<template>
  <MaterialPage>
    <article>
      <header class="">
        <h3 class="shorter-h">
          {{ $t('nav.About') }}
        </h3>
      </header>
      <section class="about-section">
        <p>
          This is a graph tutorial website
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
