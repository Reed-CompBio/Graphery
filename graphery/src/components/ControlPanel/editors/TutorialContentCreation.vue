<template>
  <ControlPageContentFrame>
    <template slot="title">
      Edit Tutorial Content
    </template>
    <template>
      <!-- not full height -->
      <div class="row full-height">
        <!-- Editor Section -->
        <div class="col-9 full-height q-pr-sm">
          <!-- title -->
          <div class="row q-mb-lg">
            <q-input
              v-model="title"
              :hint="`Tutorial URL: ${url}`"
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
            <EditorSection class="full-width"></EditorSection>
          </div>
        </div>

        <!-- Meta Section -->
        <div class="col-3 q-pl-sm">
          <!-- choose published -->
          <div id="published-chooser" class="q-mb-md">
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
          </div>

          <!-- choose authors -->
          <div id="author-chooser" class="q-mb-md">
            <InfoCard>
              <template v-slot:title>
                Authors
              </template>

              <q-select
                outlined
                use-chips
                multiple
                dense
                clearable
                v-model="authorChoice"
                :options="authorOptions"
                label="Authors"
              />
            </InfoCard>
          </div>

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
          </div>

          <!-- abstract section -->
          <div id="abstract-section" class="q-mb-md">
            <InfoCard>
              <template v-slot:title>
                Abstract
              </template>
              <q-input v-model="abstractText" outlined type="textarea" />
            </InfoCard>
          </div>

          <!-- submit section -->
          <div id="submit-section">
            <!-- TODO button action -->
            <q-btn label="Submit" class="full-width"></q-btn>
            <!-- TODO align two sections -->
          </div>
        </div>
      </div>
    </template>
  </ControlPageContentFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin.vue';
  export default {
    mixins: [loadingMixin],
    props: ['url'],
    components: {
      EditorSection: () => import('../parts/EditorSection.vue'),
      ControlPageContentFrame: () => import('../ControlPanelContentFrame.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        title: '',
        isPublished: false,
        authorChoice: [],
        authorOptions: [],
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
        abstractText: '',
      };
    },
  };
</script>
