<template>
  <MaterialPage>
    <div class="flex-center text-center">
      <h3>Welcome to Graphery</h3>
      <p class="text-subtitle1">This is a graph algorithm tutorial website.</p>
    </div>
    <q-separator></q-separator>
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
          <q-btn-dropdown size="lg" :label="$t('nav.Feedback')">
            <q-list>
              <q-item
                tag="a"
                href="https://github.com/poppy-poppy/Graphery/issues"
                target="_blank"
              >
                <q-item-section>
                  <q-item-label class="feedback-item">
                    GitHub Issues
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item
                tag="a"
                href="mailto:zengl@reed.edu?subject=Graphery%20Feedback&body=Please%20describe%20in%20detail%3A%0D%0A1.%20if%20something%20looks%20wrong%2C%20please%20tell%20us%20what%20it%20should%20be%20like%20and%20how%20we%20can%20reproduce%20the%20problem%0D%0A2.%20if%20something%20can%20be%20better%2C%20please%20tell%20us%20how%20we%20can%20improve%20and%20the%20reasons%0D%0A%0D%0AThank%20you%20so%20much!"
              >
                <q-item-section>
                  <q-item-label class="feedback-item">
                    {{ $t('nav.EmailMe') }}
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
      </div>
    </div>
    <div class="flex-center text-center text-body1">
      <p>
        You can check out our tutorials and play with graphs.
      </p>
      <p>
        You don't have an account yet, the settings will only be stored locally.
      </p>
    </div>
  </MaterialPage>
</template>

<script>
  // @ is an alias to /src

  export default {
    name: 'Home',
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
    },
  };
</script>

<style lang="sass">
  .button-wrapper
    margin: 5px 10px
  .feedback-item
    text-align: center
    font-weight: bold
</style>
