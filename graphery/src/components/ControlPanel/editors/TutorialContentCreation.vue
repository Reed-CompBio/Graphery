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
              @changes="handleEditorChanges"
              @saves="saveUploadCallback"
            ></EditorSection>

            <div id="md-editor-how-to" class="q-mt-md q-pb-xl full-width">
              <EditorHowTo />
            </div>
          </div>
        </template>

        <template v-slot:right>
          <URLCard
            :url="tutorialUrl"
            :routePath="resolvedPath"
            class="full-width"
          />
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

          <StoreLocation location="Cloud" />

          <!-- submit section -->
          <div id="submit-section">
            <SubmitButton
              :action="postValue"
              :loading="loadingContent"
              class="full-width"
            />
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
  import imageHandleMixin from '../mixins/ImageHandleMixin';
  import { apiCaller } from '@/services/apis';
  import {
    tutorialContentMutation,
    tutorialContentQuery,
  } from '@/services/queries';
  import { newModelUUID } from '@/services/params';
  import { errorDialog, resolveLink, successDialog } from '@/services/helpers';

  export default {
    mixins: [loadingMixin, pushToMixin, imageHandleMixin],
    // TODO add props to router url
    props: ['anchorId', 'contentId', 'tutorialUrl', 'lang'],
    components: {
      StoreLocation: () =>
        import('@/components/ControlPanel/parts/StoreLocationCard'),
      EditorHowTo: () => import('@/components/ControlPanel/parts/EditorHowTo'),
      SubmitButton: () =>
        import('@/components/ControlPanel/parts/SubmitButton'),
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
          tutorialAnchor: this.anchorId,
        },
      };
    },
    computed: {
      isCreatingNew() {
        return this.tutorialContentObj.id === newModelUUID;
      },
      resolvedPath() {
        return resolveLink({
          name: 'Tutorial',
          params: { url: this.tutorialUrl },
        });
      },
    },
    methods: {
      updateContentObj(raw, rendered) {
        this.tutorialContentObj.contentMd = raw;
        this.tutorialContentObj.contentHtml = rendered;
      },
      updateLocalStorage(raw, rendered) {
        this.$store.commit('edits/UPDATE_TUTORIAL_CONTENT', {
          contentId: this.tutorialContentObj.id,
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
        apiCaller(tutorialContentQuery, {
          id: this.tutorialContentObj.tutorialAnchor,
          translation: this.lang,
        })
          .then((data) => {
            if (!data || !('tutorial' in data)) {
              throw Error('Invalid data returned.');
            }

            if (!data.tutorial) {
              throw Error(`No tutorial for ID ${this.anchorId}.`);
            }

            if (data.tutorial.content.id !== this.tutorialContentObj.id) {
              if (this.tutorialContentObj.id === newModelUUID) {
                data.tutorial.content.id = newModelUUID;
              } else {
                throw Error(
                  `Invalid content ID specified: ${this.tutorialContentObj.id}`
                );
              }
            }

            this.tutorialUrl = data.tutorial.url;
            Object.assign(this.tutorialContentObj, data.tutorial.content);
            this.tutorialContentObj.authors = this.tutorialContentObj.authors.map(
              (obj) => obj.id
            );

            if (this.$refs.mdEditor) {
              this.$refs.mdEditor.initText(this.tutorialContentObj.contentMd);
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
      pushToNewPlace(id) {
        if (this.$route.params.contentId === newModelUUID) {
          this.$router.push({
            name: this.$route.name,
            params: {
              anchorId: this.tutorialContentObj.tutorialAnchor,
              contentId: id,
            },
            query: {
              lang: this.lang,
              tutorialUrl: this.tutorialUrl,
            },
          });
        }
      },
      postValue() {
        this.startLoading();
        apiCaller(tutorialContentMutation, {
          lang: this.lang,
          content: this.tutorialContentObj,
        })
          .then((data) => {
            if (!data || !('updateTutorialContent' in data)) {
              throw Error('Invalid data returned.');
            }

            if (!data.updateTutorialContent.success) {
              throw Error('Cannot update tutorial content for unknown reason.');
            }

            this.tutorialContentObj.id = data.updateTutorialContent.model.id;

            this.pushToNewPlace(this.tutorialContentObj.id);
            successDialog({
              message: 'Update Tutorial Content Successfully!',
            });
          })
          .catch((err) => {
            errorDialog({
              message: `Cannot update tutorial content. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
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
