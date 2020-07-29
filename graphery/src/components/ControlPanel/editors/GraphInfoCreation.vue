<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Graph Info Editor
    </template>
    <template>
      <div class="row full-height">
        <!-- Editor Section -->
        <div class="col-9 full-height q-pr-sm">
          <!-- title -->
          <div class="row q-mb-lg">
            <q-input v-model="graphInfoObject.title" outlined class="full-width">
              <template v-slot:prepend>
                <q-icon name="title" />
              </template>
            </q-input>
          </div>
          <!-- editor -->
          <div class="row q-my-lg" style="height: 70vh;">
            <EditorSection class="full-width" />
          </div>
        </div>

        <!-- Meta Section -->
        <div class="col-3 q-pl-sm">
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

              <!-- submit section -->
              <div id="submit-section">
                <!-- TODO button action -->
                <q-btn label="Submit" class="full-width"></q-btn>
                <!-- TODO align two sections -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import LangCard from '@/components/ControlPanel/parts/LangCard';
  export default {
    // TODO add props to router url
    props: ['id', 'url', 'lang'],
    components: {
      LangCard,
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
