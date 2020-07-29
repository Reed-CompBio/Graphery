<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Graph Info Editor
    </template>
    <template>
      <EditorFrame>
        <template v-slot:left>
          <div class="row q-mb-lg">
            <q-input
              v-model="graphInfoObject.title"
              outlined
              class="full-width"
            >
              <template v-slot:prepend>
                <q-icon name="title" />
              </template>
            </q-input>
          </div>
          <!-- editor -->
          <div class="row q-my-lg" style="height: 70vh;">
            <EditorSection class="full-width" />
          </div>
        </template>
        <template v-slot:right>
          <IDCard :id="id" class="full-width" />
          <URLCard :url="url" class="full-width" />
          <LangCard :lang="lang" class="full-width" />

          <!-- published -->
          <div id="published-chooser" class="q-mb-md">
            <InfoCard>
              <template v-slot:title>
                Published?
              </template>
              <q-checkbox
                v-model="graphInfoObject.isPublished"
                :label="graphInfoObject.isPublished ? '✅' : '❌'"
                dense
              ></q-checkbox>
            </InfoCard>
          </div>

          <!-- submit section -->
          <div id="submit-section">
            <!-- TODO button action -->
            <q-btn label="Submit" class="full-width"></q-btn>
            <!-- TODO align two sections -->
          </div>
        </template>
      </EditorFrame>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  export default {
    // TODO add props to router url
    props: ['id', 'url', 'lang'],
    components: {
      EditorFrame: () => import('../frames/EditorFrame.vue'),
      LangCard: () => import('../parts/LangCard'),
      URLCard: () => import('@/components/ControlPanel/parts/URLCard'),
      IDCard: () => import('@/components/ControlPanel/parts/IDCard'),
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      EditorSection: () => import('../parts/EditorSection.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        graphInfoObject: {
          title: '',
          isPublished: false,
          abstractMd: '',
          abstractHtml: '',
        },
      };
    },
  };
</script>
