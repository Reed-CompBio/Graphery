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
        <q-card class="q-px-md q-py-sm license-card">
          <p>
            <a
              rel="license"
              href="http://creativecommons.org/licenses/by-nc-sa/4.0/"
            >
              <img
                alt="Creative Commons License"
                style="border-width:0"
                src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png"
              />
            </a>
            <br />
            All the articles are licensed under a
            <a
              rel="license"
              href="http://creativecommons.org/licenses/by-nc-sa/4.0/"
            >
              Creative Commons Attribution-NonCommercial-ShareAlike 4.0
              International License
            </a>
          </p>
        </q-card>
      </section>
    </article>
  </MaterialPage>
</template>

<script>
  export default {
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
    },
  };
</script>

<style lang="sass">
  .about-section
    p
      font-size: 1.2rem
    .license-card
      background-color: orange
      a, a:visited
        color: white
</style>
