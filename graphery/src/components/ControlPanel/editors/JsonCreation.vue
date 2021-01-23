<template>
  <EditorFrame>
    <template v-slot:left>
      <InfoCard>
        <template v-slot:title>
          <div class="q-mb-md">
            Exec JSON
          </div>
          <div class="q-mb-md">
            <q-select
              :options="graphOptions"
              v-model="graphChoice"
              label="Select Graph"
              outlined
              map-options
              option-label="name"
              :disable="customLoading"
              :loading="customLoading"
            />
          </div>
          <div>
            <q-btn
              label="Exec Locally"
              :loading="customLoading"
              @click="execCodeOnCurrentGraphLocally"
              class="q-mr-sm"
            />
            <q-btn
              label="Exec All Locally"
              :loading="customLoading"
              @click="execCodeOnAllGraphsLocally"
              class="q-mr-sm"
            />
            <q-btn
              label="Exec All On The Cloud"
              :loading="customLoading"
              @click="execCodeOnAllGraphsOnTheCloud"
              class="q-mr-sm"
            />
          </div>
        </template>
        <div>
          <q-input
            readonly
            class="half-height-textarea"
            v-model="resultJson"
            type="textarea"
            outlined
            label="Execution Result Json (Read Only)"
            :loading="customLoading"
          />
        </div>
      </InfoCard>
    </template>
    <template v-slot:right>
      <JSONSubmissionAttentionCard />
      <SubmitButton
        class="full-width"
        :loading="customLoading"
        :action="postExecJson"
      />
    </template>
  </EditorFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin';
  import {
    executeCode,
    resultJsonGetGraphsQuery,
    resultJsonsMutation,
  } from '@/services/queries';
  import { apiCaller } from '@/services/apis';
  import {
    errorDialog,
    successDialog,
    warningDialog,
  } from '@/services/helpers';
  import PushCodeToLocalMixin from '@/components/mixins/PushCodeToLocalMixin';
  import { newModelUUID } from '@/services/params';

  export default {
    props: ['codeId', 'codeContent', 'updating'],
    mixins: [loadingMixin, PushCodeToLocalMixin],
    components: {
      JSONSubmissionAttentionCard: () =>
        import(
          '@/components/ControlPanel/parts/cards/JSONSubmissionAttentionCard'
        ),
      InfoCard: () => import('../parts/cards/InfoCard'),
      SubmitButton: () => import('../parts/buttons/SubmitButton'),
      EditorFrame: () => import('../frames/EditorFrame'),
    },
    data() {
      return {
        graphChoice: null,
        graphOptions: null,
        execResults: null,
        newResults: {},
      };
    },
    computed: {
      resultJson() {
        return (
          this.graphChoice &&
          this.execResults &&
          this.execResults[this.graphChoice.id]
        );
      },
      customLoading() {
        return this.loadingContent || this.updating;
      },
      allowSubmit() {
        if (this.graphOptions) {
          if (this.graphOptions.length === 0) {
            return false;
          }
          return true;
        } else {
          return false;
        }
      },
    },
    methods: {
      fetchTutorialGraphs() {
        if (this.codeId === newModelUUID) {
          return;
        }

        this.startLoading();
        apiCaller(resultJsonGetGraphsQuery, {
          id: this.codeId,
        })
          .then((data) => {
            if (!data || !('code' in data) || !data.code.tutorial) {
              throw Error('Invalid data returned.');
            }

            if (!data.code.tutorial.graphSet) {
              warningDialog({
                message: 'This tutorial may not have graphs associated.',
              });
            }

            this.graphOptions = data.code.tutorial.graphSet;

            if (
              !data.code.execresultjsonSet ||
              data.code.execresultjsonSet.length === 0
            ) {
              warningDialog({
                message:
                  'This tutorial may not have initial execution json results.',
              });
            }
            this.execResults = {};
            data.code.execresultjsonSet.forEach((obj) => {
              this.execResults[obj.graph.id] = obj.json;
            });

            successDialog({
              message: 'Fetched result JSON set.',
            });
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching graphs. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
      async localExec(graphJson, graphId) {
        await this.pushToLocal(
          this.codeContent,
          graphJson,
          null,
          (codeHash, execResult) => {
            this.execResults = {
              ...this.execResults,
            };
            // TODO by creating a new object, the computed property will work. Waste performance?
            this.execResults[graphId] = JSON.stringify(execResult);
          },
          null
        );
      },
      async execCodeOnCurrentGraphLocally() {
        if (this.graphChoice) {
          const graphJson = JSON.parse(this.graphChoice.cyjs);
          const graphId = this.graphChoice.id;
          this.startLoading();
          await this.localExec(graphJson, graphId);
          this.finishedLoading();
        } else {
          errorDialog({
            message: 'Please choose a graph to run code.',
          });
        }
      },
      async execCodeOnAllGraphsLocally() {
        this.startLoading();
        for (const obj of this.graphOptions) {
          await this.localExec(JSON.parse(obj.cyjs), obj.id);
        }
        this.finishedLoading();
      },
      postExecJson() {
        this.startLoading();
        apiCaller(resultJsonsMutation, {
          codeId: this.codeId,
          resultJsonDict: this.execResults,
        })
          .then((data) => {
            if (!data || !('updateResultJson' in data)) {
              throw Error('Invalid data returned.');
            }

            if (!data.updateResultJson.success) {
              throw Error('Cannot update result JSONs for unknown reason.');
            }

            successDialog({
              message: 'Update Result JSONs Successfully!',
            });
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during updating result JSONs. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
      execCodeOnAllGraphsOnTheCloud() {
        this.startLoading();
        apiCaller(executeCode, {
          codeIds: [this.codeId],
        })
          .then((data) => {
            if (!data || !('executeCode' in data)) {
              throw Error('Invalid data returned.');
            }

            if (data.executeCode.success) {
              successDialog({
                message: 'Executed all successfully!',
              });
            } else {
              for (const obj of data.executeCode.failedMissions) {
                errorDialog(
                  {
                    message: `An error occurs running code ${obj.code.name} on graph ${obj.graph.name} with error ${obj.error}`,
                  },
                  0
                );
              }
            }
          })
          .then(() => {
            this.fetchTutorialGraphs();
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during executing code OL: ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
    },
    mounted() {
      this.fetchTutorialGraphs();
    },
    watch: {
      tutorial: function() {
        this.fetchTutorialGraphs();
      },
    },
  };
</script>
