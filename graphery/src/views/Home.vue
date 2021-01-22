<template>
  <div>
    <MaterialCover :cover-title="$t('nav.Home')" />
    <MaterialPage>
      <div class="page">
        <div
          :class="['welcome-box', 'flex-center', mdRowControl]"
          class="justify-center"
        >
          <!-- FIXME: mobile breakpoint (responsive adaption)-->
          <!-- FIXME: beautify the logo -->
          <div :class="[mdColControl]" class="justify-center">
            <img :src="logoSrc" class="logo" alt="site logo" />
          </div>
          <div :class="[mdColControl]" class="graphery-text justify-center">
            <h3 class="welcome-title">
              Welcome to <span class="logo-text">GRAPHERY</span>
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
          <div
            :class="[smRowControl]"
            class="fit"
            style="justify-content: space-between"
          >
            <div
              :key="index"
              v-for="(item, index) in features"
              :class="['feature', smColControl]"
            >
              <div class="icon">
                <q-icon :name="item.icon"></q-icon>
              </div>
              <div :class="['title', smColControl]">{{ item.title }}</div>
              <div :class="['description', smColControl]">
                <p>
                  {{ item.description }}
                </p>
              </div>
            </div>
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
            title: 'Tutorials',
            description: 'Graphery is a tutorial based webservice.',
            icon: 'mdi-script-text-outline',
          },
          {
            title: 'Interactive Graphs and Customizable Code',
            description:
              'Provide interactive graphs and allow users to write their own code to interact with existing graphs',
            icon: 'mdi-cursor-default-click-outline',
          },
          {
            title: 'Visualization',
            description:
              'Execute and visualize execution results of example code and customized code',
            icon: 'mdi-eye-check-outline',
          },
        ],
      };
    },
    computed: {
      ltSmBreakpoint() {
        return this.$q.screen.lt.sm;
      },
      ltMdBreakpoint() {
        return this.$q.screen.lt.md;
      },
      smRowControl() {
        if (this.ltSmBreakpoint) {
          return 'col';
        } else {
          return 'row';
        }
      },
      mdRowControl() {
        if (this.ltMdBreakpoint) {
          return 'col';
        } else {
          return 'row';
        }
      },
      smColControl() {
        if (this.ltSmBreakpoint) {
          return 'row';
        } else {
          return 'col';
        }
      },
      mdColControl() {
        if (this.ltMdBreakpoint) {
          return 'row';
        } else {
          return 'col';
        }
      },
    },
  };
</script>

<style lang="sass" scoped>
  @import "~@/styles/home.sass"

  .page
    //background: #fff
    //padding: 30px
</style>
