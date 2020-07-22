<template>
  <div class="full-height" style="min-height: inherit;">
    <div
      class="q-pa-xl"
      style=" display: flex; flex-direction: column; min-height: inherit;"
    >
      <div id="title-section" class="q-mt-sm q-mb-xl">
        <h3 class="control-panel-h3">
          <slot name="title"></slot>
        </h3>
      </div>
      <div id="control-panel-content" style="flex-grow: 1;">
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
