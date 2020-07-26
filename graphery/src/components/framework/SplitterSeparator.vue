<template>
  <div
    :class="[
      horizontal
        ? 'splitter-separator-horizontal'
        : 'splitter-separator-vertical',
      'splitter-separator',
    ]"
  ></div>
</template>

<script>
  export default {
    props: ['horizontal'],
  };
</script>

<style lang="sass">
  $separator-height: 50px
  $separator-width: 4px
  .splitter-separator-horizontal
    border-top: $separator-width solid
    width: $separator-height

  .splitter-separator-vertical
    border-left: $separator-width solid
    height: $separator-height

  .splitter-separator:hover
    border-color: #fff

  .splitter-separator
    transition: 150ms ease-in-out
    border-radius: 25px
    border-color: #929292
</style>
