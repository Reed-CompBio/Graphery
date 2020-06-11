<template>
  <MaterialPage>
    <div class="flex-center text-center">
      <h3>Welcome to Graphery</h3>
      <p class="text-subtitle1">This is a graph algorithm tutorial website.</p>
    </div>
    <q-separator></q-separator>
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
      </div>
    </div>
    <div class="flex-center text-center text-body1">
      <p>
        You can check out our tutorials and play with graphs.
      </p>
      <p>
        You don't have an account yet, the settings will only be stored locally.
      </p>
    </div>
  </MaterialPage>
</template>

<script>
  // @ is an alias to /src

  export default {
    name: 'Home',
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
    },
  };
</script>

<style lang="sass">
  .button-wrapper
    margin: 5px 10px
</style>
