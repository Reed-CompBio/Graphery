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
  .splitter-separator-horizontal
    border-top: 4px solid #b3b3b3
    width: 10%

  .splitter-separator-vertical
    border-left: 4px solid #b3b3b3
    height: 10%

  .splitter-separator:hover
    transform: change_color(#fff)

  .splitter-separator
    transition: 300ms ease-out
    border-radius: 25px
</style>
