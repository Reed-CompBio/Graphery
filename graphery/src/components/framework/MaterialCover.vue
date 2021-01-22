<template>
  <div class="cover-wrapper flex justify-between">
    <div class="text-bold cover-text">{{ coverTitle }}</div>
    <img :src="logoPath" class="logo" alt="" />
  </div>
</template>

<script>
  export default {
    name: 'MaterialCover',
    props: {
      coverTitle: {
        type: String,
      },
      logoPath: {
        default: require('@/assets/images/compbio-lab-white.png'),
      },
    },
    data() {
      return {};
    },
  };
</script>

<style lang="sass" scoped>
  .cover-wrapper
    background-color: #A70E16
    height: 180px
    $general-opacity: .15
    .cover-text
      margin-left: 2rem
      margin-top: -2rem
      opacity: $general-opacity
      color: #fff
      font-size: 9rem

    .logo
      width: 300px
      height: 300px
      opacity: $general-opacity
      margin-right: 2rem
</style>
