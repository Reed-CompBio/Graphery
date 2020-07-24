<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Code List
    </template>
    <template>
      <q-table
        :data="tableContent"
        :columns="columns"
        :pagination="pagination"
        :loading="loadingTable"
        no-data-label="No code is found."
        row-key="id"
        separator="cell"
        class="custom-table"
      >
        <template v-slot:top>
          <RefreshButton :fetch-func="fetchCode" />
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td key="edit" :props="props">
              <OpenInEditorButton label="Edit" />
            </q-td>
            <q-td key="tutorialName" :props="props">
              {{ props.row.tutorialName }}
            </q-td>

            <q-td key="graphName" :props="props">
              {{ props.row.graphName }}
            </q-td>

            <q-td key="code" :props="props">
              <q-input
                outlined
                readonly
                type="textarea"
                v-model="props.row.code"
              />
            </q-td>

            <q-td key="json" :props="props">
              <q-input
                outlined
                readonly
                type="textarea"
                v-model="props.row.json"
              />
            </q-td>

            <q-td key="tutorialUrl" :props="props">
              <OpenInPageButton :label="props.row.tutorialUrl" />
            </q-td>

            <q-td key="graphUrl" :props="props">
              <OpenInPageButton :label="props.row.graphUrl" />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin.vue';

  export default {
    mixins: [loadingMixin],
    components: {
      ControlPanelContentFrame: () => import('../ControlPanelContentFrame.vue'),
      RefreshButton: () => import('../parts/RefreshButton'),
      OpenInPageButton: () => import('../parts/OpenInPageButton'),
      OpenInEditorButton: () => import('../parts/OpenInEditorButton'),
    },
    data() {
      return {
        columns: [
          { name: 'edit', label: 'Edit' },
          {
            name: 'tutorialName',
            label: 'Tutorial Name',
            field: 'tutorialName',
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
            name: 'graphName',
            label: 'Graph Name',
            field: 'graphName',
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
            name: 'code',
            label: 'Code',
            field: 'code',
            align: 'center',
          },
          {
            name: 'json',
            label: 'JSON',
            field: 'json',
            align: 'center',
          },
          {
            name: 'tutorialUrl',
            label: 'Tutorial URL',
            field: 'tutorialUrl',
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
        pagination: {
          sortBy: 'tutorialName',
          rowsPerPage: 10,
        },
        tableContent: [],
      };
    },
    methods: {
      fetchCode() {
        // TODO
      },
    },
  };
</script>
