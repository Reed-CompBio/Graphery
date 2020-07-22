<template>
  <ControlPageContentFrame>
    <template slot="title">
      Edit Tutorial Anchor
    </template>
    <template>
      <!-- not full height -->
      <div class="row full-height">
        <!-- Editor Section -->
        <div class="col-10 full-height q-pr-sm">
          <!-- title -->
          <div class="row q-mb-lg">
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
          <div class="row q-my-lg" style="height: 70vh;">
            <EditorSection style="width: 100%; "></EditorSection>
          </div>
        </div>

        <!-- Meta Section -->
        <div class="col-2 q-pl-sm">
          <!-- choose published -->
          <div id="published-chooser" class="q-mb-md">
            <q-card>
              <q-card-section>
                Published?
              </q-card-section>
              <q-separator />
              <q-card-section>
                <q-checkbox
                  v-model="isPublished"
                  :label="isPublished ? '✅' : '❌'"
                  dense
                ></q-checkbox>
              </q-card-section>
            </q-card>
          </div>

          <!-- choose authors -->
          <div id="author-chooser" class="q-mb-md">
            <q-card>
              <q-card-section>
                Authors
              </q-card-section>
              <q-separator></q-separator>
              <q-card-section>
                <q-select
                  outlined
                  use-chips
                  multiple
                  dense
                  v-model="authorChoice"
                  :options="authorOptions"
                  label="Authors"
                />
              </q-card-section>
            </q-card>
          </div>

          <!-- choose language -->
          <div id="lang-chooser" class="q-mb-md">
            <q-card>
              <q-card-section>
                Language
              </q-card-section>
              <q-separator />
              <q-card-section>
                <q-option-group
                  v-model="langChoice"
                  :options="langOptions"
                ></q-option-group>
              </q-card-section>
            </q-card>
          </div>

          <!-- abstract section -->
          <div id="abstract-section" class="q-mb-md">
            <q-card>
              <q-card-section>
                Abstract
              </q-card-section>
              <q-separator />
              <q-card-section>
                <q-input v-model="abstractText" outlined type="textarea" />
              </q-card-section>
            </q-card>
          </div>

          <!-- submit section -->
          <div id="submit-section">
            <!-- TODO button action -->
            <q-btn label="Submit" style="width: 100%;"></q-btn>
            <!-- TODO align two sections -->
          </div>
        </div>
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
        loading: false,
        title: '',
        isPublished: false,
        authorChoice: [],
        authorOptions: [],
        langChoice: '',
        langOptions: [
          {
            label: 'en-us',
            value: 'enus',
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
