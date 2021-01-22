<template>
  <div>
    <MaterialCover :cover-title="$t('nav.Home')" />
    <MaterialPage>
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
          <div :key="index" v-for="(item, index) in features" class="feature">
            <div class="icon">
              <q-icon :name="item.icon"></q-icon>
            </div>
            <div class="title">{{ item.title }}</div>
            <div class="description">{{ item.description }}</div>
          </div>
        </div>
      </div>
    </MaterialPage>
  </div>
</template>

<script>
  import MaterialCover from '@/components/framework/MaterialCover';
  import MaterialPage from '@/components/framework/MaterialPage';
  export default {
    name: 'Home',
    components: { MaterialPage, MaterialCover },
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
            title: 'Feature',
            description: 'description',
            icon: 'mdi-fishbowl-outline',
          },
          {
            title: 'Feature',
            description: 'description',
            icon: 'mdi-flag-checkered',
          },
        ],
      };
    },
  };
</script>

<style lang="sass" scoped>
  @import "~@/styles/home.sass"

  .page
    //background: #fff
    //padding: 30px
</style>
