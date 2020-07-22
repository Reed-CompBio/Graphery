<template>
  <div class="q-pa-xl full-height" style="min-height: inherit;">
    <div>
      <div id="title-section" class="q-mt-sm q-mb-xl">
        <h3 class="control-panel-h3">
          <slot name="title"></slot>
        </h3>
      </div>
      <div id="control-panel-content" class="q-py-sm full-height">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
  export default {};
</script>

<style lang="sass">
  .control-panel-h3
    margin: 0
</style>
