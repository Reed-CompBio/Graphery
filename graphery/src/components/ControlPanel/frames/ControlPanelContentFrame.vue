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

  .custom-table
    thead tr:first-child th:first-child
      /* bg color is important for th; just specify one */
      background-color: #fff

    td:first-child
      background-color: #f5f5dc

    th
      font-size: 16px

    th:first-child,
    td:first-child
      position: sticky
      left: 0
      z-index: 5

  .half-width-card
    width: 50%

  .half-height-textarea textarea
    height: 50vh
</style>
