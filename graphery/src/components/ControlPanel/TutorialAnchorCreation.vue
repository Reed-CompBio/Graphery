<template>
  <ControlPageContentFrame>
    <template slot="title">
      Edit Tutorial Anchor
    </template>
    <template>
      <div class="row">
        <!-- Editor Section -->
        <div class="col-10">
          <!-- title -->
          <div class="row"></div>
          <!-- editor -->
          <div class="row">
            <EditorSection></EditorSection>
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
    components: {
      EditorSection: () => import('./EditorSection'),
      ControlPageContentFrame: () => import('./ControlPanelContentFrame.vue'),
    },
  };
</script>
