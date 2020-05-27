<template>
  <MaterialPage>
    <div id="search-section">Search Bar is here</div>
    <div id="content-section">
      <div class="row">
        <div id="filter-section" class="col-3">
          Filter section
        </div>
        <div class="col-1"><q-separator vertical /></div>
        <div id="tutorial-list" class="col-8">
          Tutorial list section
        </div>
      </div>
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
