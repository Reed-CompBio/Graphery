<template>
  <MaterialPage>
    <div class="flex-center text-center">
      <h3>Welcome to Graphery</h3>
      <p class="text-subtitle1">This is a graph algorithm tutorial website.</p>
    </div>
    <q-separator></q-separator>
    <div class="row q-my-md">
      <q-btn size="lg" class="q-ml-auto">Tutorials</q-btn>
      <q-btn size="lg" class="q-mx-lg">Graphs</q-btn>
      <q-btn size="lg" class="q-mr-auto">Account</q-btn>
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
