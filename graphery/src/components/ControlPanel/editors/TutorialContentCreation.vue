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
              hint="Tutorial Title"
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
              ref="mdEditor"
              :initValue="tutorialContentObj.contentMd"
              :imgAddAction="imgAddCallback"
              :imgDelAction="imgDelCallback"
            ></EditorSection>
          </div>
        </template>

        <template v-slot:right>
          <URLCard :url="tutorialUrl" class="full-width" />
          <IDCard title="Tutorial ID" :id="anchorId" class="full-width" />
          <IDCard title="Content ID" :id="contentId" class="full-width" />
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
  import pushToMixin from '../mixins/PushToMixin.vue';
  import { apiCaller } from '@/services/apis';
  import { tutorialContentQuery } from '@/services/queries';
  import { newModelUUID } from '@/services/params';
  import { errorDialog } from '@/services/helpers';

  export default {
    mixins: [loadingMixin, pushToMixin],
    // TODO add props to router url
    props: ['anchorId', 'contentId', 'tutorialUrl', 'lang'],
    components: {
      LangCard: () => import('@/components/ControlPanel/parts/LangCard'),
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
          id: this.contentId,
          title: '',
          isPublished: false,
          authors: [],
          abstract: '',
          contentMd: '',
          contentHtml: '',
          tutorialAnchor: this.url,
        },
      };
    },
    computed: {
      isCreatingNew() {
        return this.tutorialContentObj.id === newModelUUID;
      },
    },
    methods: {
      imgAddCallback(fileName, file) {
        // TODO post lang with axios
        console.log(fileName, file);
      },
      imgDelCallback(filename, file) {
        console.log(filename, file);
      },
      fetchValue() {
        this.startLoading();
        apiCaller(tutorialContentQuery, {
          id: this.anchorId,
          translation: this.lang,
        })
          .then((data) => {
            if (!data || !('tutorial' in data)) {
              throw Error('Invalid data returned.');
            }

            if (!data.tutorial) {
              throw Error(`No tutorial for ID ${this.anchorId}.`);
            }

            if (data.tutorial.content.id !== this.contentId) {
              if (this.tutorialContentObj.id === newModelUUID) {
                data.tutorial.content.id = newModelUUID;
              } else {
                throw Error(`Invalid content ID specified: ${this.contentId}`);
              }
            }

            data.tutorial.content.tutorialAnchor = data.tutorial.url;
            Object.assign(this.tutorialContentObj, data.tutorial.content);
            this.tutorialContentObj.authors = this.tutorialContentObj.authors.map(
              (obj) => obj.id
            );

            if (this.$refs.mdEditor) {
              this.$refs.mdEditor.initValue(this.tutorialContentObj.contentMd);
            }
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching tutorial content. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
    },
    mounted() {
      this.fetchValue();
    },
  };
</script>
