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
              hint="Title"
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
              :initValue="graphInfoObject.abstractMd"
              :imgAddAction="imgAddCallback"
              :imgDelAction="imgDelCallback"
              @changes="handleEditorChanges"
              @saves="saveUploadCallback"
            />
          </div>

          <div id="md-editor-how-to" class="q-mt-md q-pb-xl full-width">
            <EditorHowTo />
          </div>
        </template>
        <template v-slot:right>
          <URLCard :url="graphUrl" class="full-width" />
          <IDCard title="Graph ID" :id="anchorId" class="full-width" />
          <IDCard title="Content ID" :id="contentId" class="full-width" />
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
  import loadingMixin from '../mixins/LoadingMixin';
  import pushToMixin from '../mixins/PushToMixin';
  import imageHandleMixin from '@/components/ControlPanel/mixins/ImageHandleMixin';
  import { newModelUUID } from '@/services/params';
  import { apiCaller } from '@/services/apis';
  import { graphInfoContentQuery } from '@/services/queries';
  import { errorDialog } from '@/services/helpers';

  export default {
    // TODO add props to router url
    mixins: [loadingMixin, pushToMixin, imageHandleMixin],
    props: ['anchorId', 'contentId', 'graphUrl', 'lang'],
    components: {
      EditorHowTo: () => import('@/components/ControlPanel/parts/EditorHowTo'),
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
          id: this.contentId,
          title: '',
          isPublished: false,
          abstractMd: '',
          abstract: '',
          graphAnchor: this.anchorId,
        },
      };
    },
    computed: {
      isCreatingNew() {
        return this.graphInfoObject.graphAnchor === newModelUUID;
      },
    },
    methods: {
      updateContentObj(raw, rendered) {
        this.graphInfoObject.abstractMd = raw;
        this.graphInfoObject.abstract = rendered;
      },
      updateLocalStorage(raw, rendered) {
        this.$store.commit('edits/UPDATE_GRAPH_INFO_CONTENT', {
          contentId: this.graphInfoObject.id,
          content: {
            raw,
            rendered,
          },
        });
      },
      handleEditorChanges(raw, rendered) {
        this.updateContentObj(raw, rendered);
        this.updateLocalStorage(raw, rendered);
      },
      fetchValue() {
        this.startLoading();

        apiCaller(graphInfoContentQuery, {
          id: this.graphInfoObject.graphAnchor,
          translation: this.lang,
        })
          .then((data) => {
            if (!data || !('graph' in data)) {
              throw Error('Invalid data returned.');
            }

            if (!data.graph) {
              throw Error(`No graph for ID ${this.anchorId}.`);
            }

            if (data.graph.content.id !== this.graphInfoObject.id) {
              if (this.graphInfoObject.id === newModelUUID) {
                data.graph.content.id = newModelUUID;
              } else {
                throw Error(
                  `Invalid content ID Specified ${this.graphInfoObject.id}`
                );
              }
            }

            this.graphUrl = data.graph.url;
            Object.assign(this.graphInfoObject, data.graph.content);

            if (this.$refs.mdEditor) {
              this.$refs.mdEditor.initText(this.graphInfoObject.abstractMd);
            }
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching graph content. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
      postValue() {
        //
      },
      saveUploadCallback() {
        this.postValue();
      },
    },
    mounted() {
      this.fetchValue();
    },
  };
</script>
