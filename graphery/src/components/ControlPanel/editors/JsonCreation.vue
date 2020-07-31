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
              :disable="loadingContent"
              :loading="loadingContent"
            />
          </div>
          <div>
            <q-btn label="Exec" :loading="loadingContent" class="q-mr-sm" />
            <q-btn
              label="Exec Locally"
              :loading="loadingContent"
              @click="execCodeOnCurrentGraph"
              class="q-mr-sm"
            />
            <q-btn label="Exec All" :loading="loadingContent" class="q-mr-sm" />
            <q-btn
              label="Exec All Locally"
              :loading="loadingContent"
              @click="execCodeOnAllGraphs"
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
            :loading="loadingContent"
          />
        </div>
      </InfoCard>
    </template>
    <template v-slot:right>
      <SubmitButton
        class="full-width"
        :loading="loadingContent"
        :action="postExecJson"
      />
    </template>
  </EditorFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin';
  import { resultJsonGetGraphsQuery } from '@/services/queries';
  import { apiCaller } from '@/services/apis';
  import { errorDialog, warningDialog } from '@/services/helpers';
  import pushCodeToLocalMixin from '@/components/mixins/PushCodeToLocalMixin';

  export default {
    props: ['codeId', 'codeContent'],
    mixins: [loadingMixin, pushCodeToLocalMixin],
    components: {
      InfoCard: () => import('../parts/InfoCard'),
      SubmitButton: () => import('../parts/SubmitButton'),
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
          this.newResults[this.graphChoice.id] &&
          this.execResults &&
          this.execResults[this.graphChoice.id]
        );
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
      localExec(graphJson, graphId) {
        this.pushToLocal(
          this.codeContent,
          graphJson,
          this.startLoading,
          (codeHash, execResult) => {
            console.log(graphId, execResult);
            this.newResults[graphId] = execResult;
          },
          this.finishedLoading
        );
      },
      execCodeOnCurrentGraph() {
        if (this.graphChoice) {
          const graphJson = JSON.parse(this.graphChoice.cyjs);
          const graphId = this.graphChoice.id;

          this.localExec(graphJson, graphId);
        } else {
          errorDialog({
            message: 'Please choose a graph to run code.',
          });
        }
      },
      execCodeOnAllGraphs() {
        //
      },
      postExecJson() {
        //
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
