<template>
  <ControlPageContentFrame>
    <template slot="title">
      Edit Tutorial Content
    </template>
    <template>
      <EditorFrame>
        <template v-slot:left>
          <!-- title -->
          <div class="row q-mb-lg">
            <q-input
              v-model="tutorialContentObj.title"
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
            <EditorSection
              class="full-width"
              :imgAddAction="imgAddCallback"
            ></EditorSection>
          </div>
        </template>

        <template v-slot:right>
          <URLCard :url="url" class="full-width" />
          <IDCard :id="id" class="full-width" />
          <LangCard :lang="lang" class="full-width" />

          <!-- choose published -->
          <div id="published-chooser" class="q-mb-md">
            <InfoCard>
              <template v-slot:title>
                Published?
              </template>
              <q-checkbox
                v-model="tutorialContentObj.isPublished"
                :label="tutorialContentObj.isPublished ? '✅' : '❌'"
                dense
              ></q-checkbox>
            </InfoCard>
          </div>

          <!-- choose authors -->
          <AuthorSelection v-model="tutorialContentObj.authors" />

          <!-- abstract section -->
          <div id="abstract-section" class="q-mb-md">
            <InfoCard>
              <template v-slot:title>
                Abstract
              </template>
              <q-input
                v-model="tutorialContentObj.abstract"
                outlined
                type="textarea"
              />
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
  </ControlPageContentFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin.vue';
  import LangCard from '@/components/ControlPanel/parts/LangCard';
  export default {
    mixins: [loadingMixin],
    // TODO add props to router url
    props: ['id', 'url', 'lang'],
    components: {
      LangCard,
      URLCard: () => import('../parts/URLCard.vue'),
      AuthorSelection: () => import('../parts/AuthorSelection.vue'),
      IDCard: () => import('../parts/IDCard.vue'),
      ControlPageContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      EditorFrame: () => import('../frames/EditorFrame.vue'),
      EditorSection: () => import('../parts/EditorSection.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        tutorialContentObj: {
          title: '',
          tutorialAnchor: this.url,
          isPublished: false,
          authors: [],
          abstract: '',
          contentMd: '',
          contentHtml: '',
        },
      };
    },
    methods: {
      imgAddCallback(fileName, file) {
        console.log(fileName, file);
      },
    },
  };
</script>
