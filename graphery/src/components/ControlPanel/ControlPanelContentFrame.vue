<template>
  <div class="full-height q-pa-xl">
    <div id="title-section" class="q-my-md">
      <h3 class="control-panel-h3">
        <slot name="title"></slot>
      </h3>
    </div>
    <div id="control-panel-content" class="q-my-md">
      <slot></slot>
    </div>
  </div>
</template>

<script>
  export default {};
</script>

<style lang="sass">
  #control-panel-h3
    margin: 0
</style>
