<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Graph Editor
    </template>
    <template>
      <EditorFrame>
        <template v-slot:left>
          <div class="row full-width">
            <IDCard :id="graphObj.id" class="full-width" />
            <div class="col-6 q-pr-sm">
              <q-input
                outlined
                v-model="graphObj.url"
                hint="please input URL. Do not start or end it with -_."
                label="Graph URL"
                :disable="!isCreatingNewGraph"
              ></q-input>
            </div>
            <div class="col-6 q-pl-sm">
              <q-input
                outlined
                v-model="graphObj.name"
                hint="Please enter a unique name."
                label="Graph Name"
              ></q-input>
            </div>
          </div>
          <div class="row full-width q-mt-md">
            <!-- TODO set an appropriate -->
            <q-card class="full-width q-mb-md">
              <q-input
                class="half-height-textarea"
                type="textarea"
                label="Graph JSON"
                outlined
                v-model="graphObj.cyjs"
              ></q-input>
            </q-card>
            <q-file
              v-model="uploadFile"
              outlined
              use-chips
              counter
              clearable
              :filter="checkFileType"
              @rejected="fileRejected"
            >
              <template v-slot:prepend>
                <q-icon name="attach_file" />
              </template>
              <template v-slot:after>
                <!-- TODO button action -->
                <q-btn round dense flat icon="send" />
              </template>
            </q-file>
          </div>
        </template>
        <template v-slot:right>
          <InfoCard>
            <template v-slot:title>
              Published
            </template>
            <q-checkbox
              v-model="graphObj.isPublished"
              :label="graphObj.isPublished ? '✅' : '❌'"
            />
          </InfoCard>

          <InfoCard>
            <template v-slot:title>
              Authors
            </template>
            <q-select
              multiple
              use-chips
              clearable
              v-model="graphObj.authors"
              :options="authorOptions"
            ></q-select>
          </InfoCard>

          <InfoCard>
            <template v-slot:title>
              Categories
            </template>
            <q-select
              multiple
              use-chips
              clearable
              v-model="graphObj.categories"
              :options="categoryOptions"
            ></q-select>
          </InfoCard>

          <InfoCard>
            <template v-slot:title>
              Tutorials
            </template>
            <!-- TODO add a confirmation dialog during deleting tutorials -->
            <q-select
              multiple
              use-chips
              v-model="graphObj.tutorials"
              :options="tutorialOptions"
            ></q-select>
          </InfoCard>

          <q-btn class="half-width-card" label="Submit"></q-btn>
        </template>
      </EditorFrame>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { errorDialog } from '../../../services/helpers';
  import { newModelUUID } from '../../../services/params';
  import IDCard from '../parts/IDCard';

  export default {
    props: ['id'],
    components: {
      IDCard,
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame'),
      EditorFrame: () => import('../frames/EditorFrame.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        graphObj: {
          id: this.id,
          url: '',
          name: '',
          cyjs: '',
          isPublished: false,
          authors: [],
          categories: [],
          tutorials: [],
        },
        authorOptions: [],
        categoryOptions: [],
        tutorialOptions: [],
        uploadFile: [],
      };
    },
    computed: {
      isCreatingNewGraph() {
        return this.id === newModelUUID;
      },
    },
    methods: {
      checkFileType(files) {
        return files.filter((file) => file.type === 'application/json');
      },
      fileRejected(rejectedEntries) {
        console.log(rejectedEntries);
        errorDialog({
          message: `${rejectedEntries[0].file.name} is not a JSON file.`,
        });
      },
    },
  };
</script>
