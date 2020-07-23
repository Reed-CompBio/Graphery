<template>
  <ControlPanelContentFrame>
    <template slot="title">
      Graphs
    </template>
    <template>
      <q-table
        :data="tableContent"
        :columns="columns"
        :pagination="pagination"
        :loading="loadingTable"
        no-data-label="No graphs are found"
        row-key="id"
        separator="cell"
        class="custom-table"
      >
        <template v-slot:top>
          <RefreshButton :fetch-func="fetchGraphs" />
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <!-- name -->
            <q-td key="name" :props="props">
              <OpenInEditorButton :label="props.row.name" />
            </q-td>

            <!-- published -->
            <q-td key="isPublished" :props="props">
              {{ props.row.isPublished ? '✅' : '❌' }}
            </q-td>

            <!-- priority -->
            <q-td key="priority" :props="props">
              {{ props.row.priority }}
            </q-td>

            <!-- authors -->
            <q-td key="authors" :props="props">
              <q-select
                multiple
                use-chips
                readonly
                :option="props.row.authors"
                v-model="props.row.authors"
              ></q-select>
            </q-td>

            <!-- tutorials -->
            <q-td key="tutorials" :props="props">
              <q-select
                multiple
                use-chips
                readonly
                :options="props.row.tutorials"
                v-model="props.row.tutorials"
              ></q-select>
            </q-td>

            <!-- cyjs -->
            <q-td key="cyjs" :props="props">
              <q-input v-model="props.row.cyjs" type="textarea" readonly>
              </q-input>
            </q-td>

            <!-- url -->
            <q-td key="url" :props="props">
              <OpenInPageButton :label="props.row.url" />
            </q-td>

            <!-- id -->
            <q-td key="id" :props="props">
              {{ props.row.id }}
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { apiCaller } from '../../../services/apis';
  import { graphListQuery } from '../../../services/queries';
  import { errorDialog } from '../../../services/helpers';
  import loadingMixin from './LoadingMixin.vue';

  export default {
    mixins: [loadingMixin],
    components: {
      ControlPanelContentFrame: () => import('../ControlPanelContentFrame.vue'),
      RefreshButton: () => import('../parts/RefreshButton'),
      OpenInEditorButton: () => import('../parts/OpenInEditorButton'),
      OpenInPageButton: () => import('../parts/OpenInPageButton'),
    },
    data() {
      return {
        columns: [
          {
            name: 'name',
            label: 'name',
            field: 'name',
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
            name: 'priority',
            label: 'Priority',
            field: 'priority',
            align: 'center',
          },
          {
            name: 'authors',
            label: 'Authors',
            field: 'authors',
            align: 'center',
          },
          {
            name: 'tutorials',
            label: 'Tutorials',
            // TODO change this
            field: 'tutorials',
            align: 'center',
          },
          {
            name: 'cyjs',
            label: 'CYJS',
            field: 'cyjs',
            align: 'center',
            style: 'min-width: 200px;',
          },
          {
            name: 'url',
            label: 'URL',
            field: 'url',
            align: 'center',
            // TODO add typewriter font style
          },
          {
            name: 'id',
            label: 'ID',
            field: 'id',
            align: 'center',
            required: true,
            // TODO add typewriter font style
          },
        ],
        pagination: {
          sortBy: 'name',
          rowsPerPage: 10,
        },
        tableContent: [],
      };
    },
    methods: {
      fetchGraphs() {
        this.startLoading();
        apiCaller(graphListQuery)
          .then(([data, errors]) => {
            if (errors) {
              throw Error(errors);
            }

            if (!data || !('allGraphInfo' in data)) {
              throw Error('Invalid data returned');
            }

            this.tableContent = data['allGraphInfo'].map((obj) => {
              obj.tutorials = obj.tutorials.map((o) => o.name);
              return obj;
            });
          })
          .catch((err) => {
            this.tableContent = [];
            errorDialog({
              message: `Cannot load graphs. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
    },
    mounted() {
      this.fetchGraphs();
    },
  };
</script>
