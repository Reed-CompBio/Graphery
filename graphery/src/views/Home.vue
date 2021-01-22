<template>
  <div class="page">
    <div class="welcome-box flex-center">
      <!-- FIXME: mobile breakpoint (responsive adaption)-->
      <!-- FIXME: beautify the logo -->
      <img :src="logoSrc" class="logo" alt="" />
      <div class="graphery-text">
        <h3 class="welcome-title">
          Welcome to <br /><span class="logo-text">GRAPHERY</span>
        </h3>
        <div class="home-intro-text">
          <p>
            This is a interactive graph algorithm tutorial website.
          </p>
          <p>
            Check out our tutorials and play with graphs.
          </p>
          <p>
            More info is listed in
            <router-link :to="{ name: 'About' }"> About </router-link>
          </p>
        </div>
      </div>
    </div>
    <q-separator />
    <div class="quick-facts flex-center">
      <div :key="item.title" v-for="item in features" class="feature">
        <div class="icon">
          <q-icon :name="item.icon"></q-icon>
        </div>
        <div class="title">{{ item.title }}</div>
        <div class="description">{{ item.description }}</div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Home',
    metaInfo() {
      const titleText = this.$t('nav.Home');
      return { title: titleText };
    },

    data() {
      return {
        logoSrc: require('@/assets/images/compbio-lab.png'),
        features: [
          {
            title: 'Tutorial',
            description: 'Graphery is a tutorial based webservice.',
            icon: 'mdi-cat',
          },
          {
            title: 'Interactive',
            description: 'description',
            icon: 'mdi-cursor-default-click-outline',
          },
          {
            title: 'Customizable',
            description: 'description',
            icon: 'mdi-move-resize-variant',
          },
        ],
      };
    },
  };
</script>

<style lang="sass">
  @import "~@/styles/home.sass"

  .page
    background: #fff
    padding: 30px
</style>
