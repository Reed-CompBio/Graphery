<template>
  <ControlPageContentFrame>
    <template slot="title">
      Edit Tutorial Anchor
    </template>
    <template>
      <!-- not full height -->
      <div class="row full-height">
        <!-- Editor Section -->
        <div class="col-10 full-height">
          <!-- title -->
          <div class="row q-my-lg">
            <q-input
              v-model="title"
              :hint="`URL: ${url}`"
              outlined
              style="width: 100%"
            >
              <template v-slot:prepend>
                <q-icon name="title" />
              </template>
            </q-input>
          </div>
          <!-- editor -->
          <div class="row q-my-lg">
            <EditorSection style="width: 100%"></EditorSection>
          </div>
        </div>

        <!-- Meta Section -->
        <div class="col-2"></div>
      </div>
    </template>
  </ControlPageContentFrame>
</template>

<script>
  export default {
    props: ['url'],
    components: {
      EditorSection: () => import('./EditorSection'),
      ControlPageContentFrame: () => import('./ControlPanelContentFrame.vue'),
    },
    data() {
      return {
        title: '',
      };
    },
  };
</script>
