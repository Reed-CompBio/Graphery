<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Graph Info
    </template>
    <q-table :data="tableContent" :columns="columns">
      <template v-slot:top>
        <RefreshButton :fetch-func="fetchGraphInfo" class="q-mr-sm" />
        <LangSelector
          :current-lang="tableLang"
          :change-callback="changeTableLang"
        />
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="title" :props="props">
            <OpenInEditorButton :label="props.row.title" />
          </q-td>

          <q-td key="isPublished" :props="props">
            {{ props.row.isPublished ? '✅' : '❌' }}
          </q-td>

          <q-td key="abstract" :props="props">
            <q-input v-model="props.row.abstract" type="textarea" readonly />
          </q-td>

          <q-td key="tutorialName" :props="props">
            {{ props.row.tutorialName }}
          </q-td>

          <q-td key="graphUrl" :props="props">
            {{ props.row.graphUrl }}
          </q-td>

          <q-td key="id" :props="props">
            {{ props.row.id }}
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </ControlPanelContentFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin.vue';
  import tableLangMixin from '../mixins/TableLangMixin.vue';
  import OpenInEditorButton from '../parts/OpenInEditorButton';
  import { apiCaller } from '../../../services/apis';

  export default {
    mixins: [loadingMixin, tableLangMixin],
    components: {
      OpenInEditorButton,
      ControlPanelContentFrame: () => import('../ControlPanelContentFrame.vue'),
      RefreshButton: () => import('../parts/RefreshButton.vue'),
      LangSelector: () => import('../parts/LangSelector.vue'),
    },
    data() {
      return {
        columns: [
          {
            name: 'title',
            label: 'title',
            field: 'title',
            align: 'center',
            sortable: true,
            sort: (a, b) => {
              if (a === b) {
                return 0;
              }

              return a < b ? -1 : 1;
            },
          },
          {
            name: 'isPublished',
            label: 'Published?',
            field: 'isPublished',
            align: 'center',
          },
          {
            name: 'abstract',
            label: 'Abstract',
            field: 'abstract',
            align: 'center',
          },
          {
            name: 'graphName',
            label: 'Graph Name',
            field: 'graphName',
            align: 'center',
          },
          {
            name: 'graphUrl',
            label: 'Graph URL',
            field: 'graphUrl',
            align: 'center',
          },
          {
            name: 'id',
            label: 'ID',
            field: 'id',
            align: 'center',
            required: true,
          },
        ],
        tableContent: [],
        pagination: {
          sortBy: 'title',
          rowsPerPage: 10,
        },
      };
    },
    computed: {
      requestVariable() {
        return {
          translation: this.tableLang,
        };
      },
    },
    methods: {
      fetchGraphInfo() {
        this.startLoading();
        apiCaller();
      },
    },
  };
</script>
