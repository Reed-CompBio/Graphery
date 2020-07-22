<template>
  <ControlPanelContentFrame>
    <template slot="title">
      Tutorials
    </template>
    <template>
      <q-table
        :data="tableContent"
        :columns="columns"
        :pagination="pagination"
        :loading="loadingTutorials"
        no-data-label="No tutorials are found."
        row-key="id"
        separator="cell"
        class="custom-table"
      >
        <template v-slot:top>
          <q-btn
            icon="refresh"
            @click.prevent="fetchTutorials"
            label="Refresh"
          ></q-btn>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <!-- tutorial name -->
            <q-td key="name" :props="props">
              <q-btn :label="props.row.name" flat>
                <SwitchTooltip text="Open In Editor"></SwitchTooltip>
              </q-btn>
            </q-td>

            <!-- tutorial published -->
            <q-td key="isPublished" :props="props">
              {{ props.row.isPublished ? '✅' : '❌' }}
            </q-td>

            <!-- tutorial url -->
            <q-td key="url" :props="props">
              <q-btn :label="props.row.url" flat>
                <SwitchTooltip text="Open Page"></SwitchTooltip>
              </q-btn>
            </q-td>

            <!-- tutorial id -->
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
  import { apiCaller } from '../../services/apis';
  import { tutorialAnchorsQuery } from '../../services/queries';
  import { errorDialog } from '../../services/helpers';

  export default {
    components: {
      ControlPanelContentFrame: () => import('./ControlPanelContentFrame.vue'),
      SwitchTooltip: () => import('@/components/framework/SwitchTooltip.vue'),
    },
    data() {
      return {
        columns: [
          {
            name: 'name',
            label: 'Name',
            field: 'name',
            align: 'center',
            sortable: true,
            // Change this. Use custom title sorting: T(number), compare (number)
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
          rowsPerPage: 20,
        },
        loadingTutorials: false,
        tableContent: [],
        // TODO add trans to no data label
      };
    },
    methods: {
      startLoading() {
        this.loadingTutorials = true;
      },
      finishedLoading() {
        this.loadingTutorials = false;
      },
      fetchTutorials() {
        this.startLoading();
        apiCaller(tutorialAnchorsQuery)
          .then(([data, errors]) => {
            if (errors) {
              throw Error(errors);
            }

            if (!data || !('allTutorialInfo' in data)) {
              throw Error('Invalid data returned');
            }

            this.tableContent = data['allTutorialInfo'];
          })
          .catch((err) => {
            this.tableContent = [];
            errorDialog({
              message: `Cannot load tutorials. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
    },
    mounted() {
      this.fetchTutorials();
    },
  };
</script>
