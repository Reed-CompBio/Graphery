<template>
  <div class="cover-wrapper flex justify-between">
    <div class="text-bold cover-text" v-if="$q.screen.gt.sm">
      {{ coverTitle }}
    </div>
    <div>
      <img :src="logoPath" class="logo" alt="" />
    </div>
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
  $water-mark-opacity: .15

  .cover-wrapper
    background-color: #A70E16
    height: 180px
    .cover-text
      margin-left: 2rem
      margin-top: -2rem
      opacity: $water-mark-opacity
      color: #fff
      font-size: 9rem

    .logo
      width: 300px
      height: 300px
      opacity: $water-mark-opacity
      margin-right: 2.2rem
</style>
