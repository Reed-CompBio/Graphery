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
            />
          </div>
          <div>
            <q-btn
              label="Add Graph"
              :loading="loadingContent"
              class="q-mr-sm"
            />
            <q-btn label="Exec" :loading="loadingContent" class="q-mr-sm" />
            <q-btn
              label="Exec Locally"
              :loading="loadingContent"
              class="q-mr-sm"
            />
            <q-btn label="Exec All" :loading="loadingContent" class="q-mr-sm" />
            <q-btn
              label="Exec All Locally"
              :loading="loadingContent"
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
      <SubmitButton class="full-width" :action="postExecJson" />
    </template>
  </EditorFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin';
  export default {
    props: ['codeId'],
    mixins: [loadingMixin],
    components: {
      InfoCard: () => import('../parts/InfoCard'),
      SubmitButton: () => import('../parts/SubmitButton'),
      EditorFrame: () => import('../frames/EditorFrame'),
    },
    data() {
      return {
        graphChoice: null,
        graphOptions: null,
      };
    },
    computed: {
      resultJson() {
        return this.graphChoice && this.graphChoice.json;
      },
    },
    methods: {
      postExecJson() {
        //
      },
    },
  };
</script>
