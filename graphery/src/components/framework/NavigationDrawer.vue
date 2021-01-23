<template>
  <q-drawer
    overlay
    behavior="mobile"
    side="right"
    :persistent="false"
    v-model="drawer"
  >
    <q-list>
      <q-card class="q-py-lg" to="/">
        <q-card-section>
          <q-item>
            <q-item-section avatar>
              <q-avatar class="mr-2">
                <img :src="logo" alt="Reed CompBio Logo" />
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <div class="site-logo">
                {{ siteName }}
              </div>
            </q-item-section>
          </q-item>
        </q-card-section>
      </q-card>
      <div class="q-pt-md">
        <q-item
          v-for="button in buttons"
          :key="button.name"
          :to="{ name: button.name }"
          exact
          class="q-pl-xl"
        >
          <q-item-section avatar>
            <q-icon :name="button.icon" size="md"></q-icon>
          </q-item-section>
          <q-item-section>
            <q-item-label header style="text-transform: uppercase">{{
              $t(`nav.${button.name}`)
            }}</q-item-label>
          </q-item-section>
        </q-item>
      </div>
    </q-list>
  </q-drawer>
</template>

<script>
  import { siteName, navigationButtons } from '@/store/states/meta';
  import { mapState } from 'vuex';

  export default {
    data() {
      return {
        siteName,
        logo: require('@/assets/images/reed-compbio-logo.png'),
        buttons: navigationButtons,
      };
    },
    computed: {
      ...mapState({
        drawerState: (state) => state.drawer,
      }),
      // temporary workaround
      drawer: {
        set(d) {
          if (!d) {
            this.$store.dispatch('changeDrawerState', d);
          }
        },
        get() {
          return this.drawerState;
        },
      },
    },
  };
</script>

<style lang="sass" scoped>
  .site-logo
    text-transform: uppercase
    font-family: "Amiri", serif
    font-size: 2.2rem
    text-align: center
</style>
