<template>
  <MaterialPage>
    <div class="flex-center text-center ">
      <h3>Welcome to Graphery</h3>
      <div class="home-intro-text">
        <p>
          This is a interactive graph algorithm tutorial website.
        </p>
        <p>
          Check out our tutorials and play with graphs.
        </p>
        <p>
          More info is listed in
          <router-link :to="{ name: 'About' }"> About </router-link>
        </p>
      </div>
    </div>
    <q-separator />
    <div class="q-mx-auto">
      <div
        :class="{
          'flex-center': true,
          'q-my-md': true,
          row: $q.screen.gt.xs,
          column: $q.screen.lt.sm,
        }"
      >
        <div class="button-wrapper">
          <q-btn size="lg" :to="{ name: 'Tutorials' }" exact>
            {{ $t('nav.Tutorials') }}
          </q-btn>
        </div>
        <div class="button-wrapper">
          <q-btn size="lg" :to="{ name: 'Graphs' }" exact>
            {{ $t('nav.Graphs') }}
          </q-btn>
        </div>
        <div class="button-wrapper">
          <q-btn size="lg" :to="{ name: 'Account' }" exact>
            {{ $t('nav.Account') }}
          </q-btn>
        </div>
        <div class="button-wrapper">
          <FeedbackDropdown />
        </div>
      </div>
    </div>
  </MaterialPage>
</template>

<script>
  export default {
    name: 'Home',
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
      FeedbackDropdown: () =>
        import('@/components/framework/FeedbackDropdown.vue'),
    },
  };
</script>

<style lang="sass">
  .button-wrapper
    margin: 5px 10px
  .feedback-item
    text-align: center
    font-weight: bold
  .home-intro-text
    font-size: 18px
</style>
