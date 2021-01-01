<template>
  <!--  <MaterialPage>-->
  <div class="page">
    <!-- <div class="flex-center text-center">-->
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
      <div class="feature">
        <div class="icon">
          <q-icon name="announcement"></q-icon>
        </div>
        <div class="title">Feature</div>
        <div class="description">Description</div>
      </div>
      <div class="feature">
        <div class="icon">
          <q-icon name="announcement"></q-icon>
        </div>
        <div class="title">Feature</div>
        <div class="description">Description</div>
      </div>
      <div class="feature">
        <div class="icon">
          <q-icon name="announcement"></q-icon>
        </div>
        <div class="title">Feature</div>
        <div class="description">Description</div>
      </div>
    </div>
    <!-- TODO:Alter these buttons below-->
    <div class="q-mx-auto">
      <div
        :class="{
          'flex-center': true,
          'q-my-md': true,
          row: $q.screen.gt.xs,
          column: $q.screen.lt.sm,
        }"
      >
        <div class="button-wrapper">
          <q-btn size="lg" :to="{ name: 'Tutorials' }" exact>
            {{ $t('nav.Tutorials') }}
          </q-btn>
        </div>
        <div class="button-wrapper">
          <q-btn size="lg" :to="{ name: 'Graphs' }" exact>
            {{ $t('nav.Graphs') }}
          </q-btn>
        </div>
        <div class="button-wrapper">
          <q-btn size="lg" :to="{ name: 'Account' }" exact>
            {{ $t('nav.Account') }}
          </q-btn>
        </div>
        <div class="button-wrapper">
          <FeedbackDropdown />
        </div>
      </div>
    </div>
  </div>
  <!--  </MaterialPage>-->
</template>

<script>
  export default {
    name: 'Home',
    metaInfo() {
      const titleText = this.$t('nav.Home');
      return { title: titleText };
    },
    components: {
      // MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
      FeedbackDropdown: () =>
        import('@/components/framework/FeedbackDropdown.vue'),
    },
    data() {
      return {
        logoSrc: require('@/assets/images/compbio-lab.png'),
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
