<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Graph Editor
    </template>
    <template>
      <div class="row">
        <div class="col-8 q-pr-sm">
          <div class="row full-width">
            <div class="col-6 q-pr-sm">
              <q-input
                outlined
                v-model="graphUrl"
                hint="please input URL. Do not start or end it with -_."
                label="Graph URL"
                :disable="!isCreatingNewGraph"
              ></q-input>
            </div>
            <div class="col-6 q-pl-sm">
              <q-input
                outlined
                v-model="graphName"
                hint="Please enter a unique name."
                label="Graph Name"
              ></q-input>
            </div>
          </div>
          <div class="row full-width q-mt-md">
            <!-- TODO set an appropriate -->
            <q-card class="full-width q-mb-md">
              <q-input
                type="textarea"
                shadow-text="Graph JSON"
                outlined
                v-model="cyjs"
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
        </div>
        <div class="col-4 q-pl-sm">
          <InfoCard class="half-width-card">
            <template v-slot:title>
              Published
            </template>
            <q-checkbox
              v-model="graphPublished"
              :label="graphPublished ? '✅' : '❌'"
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
              v-model="authorChoices"
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
              v-model="categoryChoices"
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
              v-model="tutorialChoices"
              :options="tutorialOptions"
            ></q-select>
          </InfoCard>

          <q-btn class="half-width-card" label="Submit"></q-btn>
        </div>
      </div>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { errorDialog } from '../../../services/helpers';

  export default {
    props: ['url'],
    components: {
      ControlPanelContentFrame: () => import('../ControlPanelContentFrame'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        cyjs: '',
        graphUrl: '',
        graphName: '',
        graphPublished: false,
        authorChoices: [],
        authorOptions: [],
        categoryChoices: [],
        categoryOptions: [],
        tutorialChoices: [],
        tutorialOptions: [],
        uploadFile: [],
      };
    },
    computed: {
      isCreatingNewGraph() {
        return this.url === '-new-';
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
