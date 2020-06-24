<template>
  <MaterialPage>
    <div>
      <h3 class="shorter-h">
        {{ $t('nav.Account') }}
      </h3>
    </div>
    <div>
      <p>Coming Soon</p>
    </div>
  </MaterialPage>
</template>

<script>
  export default {
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
    },
  };
</script>
