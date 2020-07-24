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
            <q-input
              v-model="title"
              :hint="`Graph URL: ${url}`"
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
        </div>

        <!-- Meta Section -->
        <div class="col-3 q-pl-sm">
          <div id="published-chooser" class="q-mb-md">
            <!-- published -->
            <InfoCard>
              <template v-slot:title>
                Published?
              </template>
              <q-checkbox
                v-model="isPublished"
                :label="isPublished ? '✅' : '❌'"
                dense
              ></q-checkbox>
            </InfoCard>

            <!-- choose language -->
            <div id="lang-chooser" class="q-mb-md">
              <InfoCard>
                <template v-slot:title>
                  Language
                </template>
                <q-option-group
                  v-model="langChoice"
                  :options="langOptions"
                ></q-option-group>
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
  export default {
    props: ['url'],
    components: {
      ControlPanelContentFrame: () => import('../ControlPanelContentFrame.vue'),
      EditorSection: () => import('../parts/EditorSection.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        title: '',
        isPublished: false,
        langChoice: '',
        langOptions: [
          {
            label: 'en-us',
            value: 'en-us',
          },
          {
            label: 'zh-cn',
            value: 'zh-cn',
          },
        ],
      };
    },
  };
</script>
