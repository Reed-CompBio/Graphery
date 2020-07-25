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
        :expanded.sync="expanded"
      >
        <template v-slot:top>
          <RefreshButton :fetch-func="fetchCode" />
        </template>
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th auto-width>
              More
            </q-th>
            <q-th v-for="col in props.cols" :key="col.name" :props="props">
              {{ col.label }}
            </q-th>
          </q-tr>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td auto-width class="text-center">
              <q-btn
                size="sm"
                color="accent"
                round
                dense
                @click="props.expand = !props.expand"
                :icon="props.expand ? 'remove' : 'add'"
              />
            </q-td>
            <q-td key="tutorialName" :props="props">
              {{ props.row.tutorialName }}
            </q-td>

            <q-td key="code" :props="props">
              <q-input
                outlined
                readonly
                type="textarea"
                v-model="props.row.code"
              />
              <OpenInEditorButton label="Edit" class="q-mt-sm" />
            </q-td>

            <q-td key="tutorialUrl" :props="props">
              <OpenInPageButton :label="props.row.tutorialUrl" />
            </q-td>

            <q-td key="id" :props="props">
              {{ props.row.id }}
            </q-td>
          </q-tr>

          <!-- Expand info -->
          <q-tr v-show="props.expand" :props="props">
            <q-td colspan="100%">
              <div class="text-left">Currently Not Available</div>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin.vue';
  import { apiCaller } from '../../../services/apis';
  import { codeListQuery } from '../../../services/queries';
  import { errorDialog } from '../../../services/helpers';

  export default {
    mixins: [loadingMixin],
    components: {
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      RefreshButton: () => import('../parts/RefreshButton'),
      OpenInPageButton: () => import('../parts/OpenInPageButton'),
      OpenInEditorButton: () => import('../parts/OpenInEditorButton'),
    },
    data() {
      return {
        columns: [
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
            name: 'code',
            label: 'Code',
            field: 'code',
            align: 'center',
          },
          {
            name: 'tutorialUrl',
            label: 'Tutorial URL',
            field: 'tutorialUrl',
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
        expanded: [],
        pagination: {
          sortBy: 'tutorialName',
          rowsPerPage: 10,
        },
        tableContent: [],
      };
    },
    methods: {
      fetchCode() {
        this.startLoading();

        apiCaller(codeListQuery)
          .then(([data, errors]) => {
            if (errors) {
              throw Error(errors);
            }

            if (!data || !('allCode' in data)) {
              throw Error('Invalid data returned.');
            }

            this.tableContent = data['allCode'].map((obj) => {
              return {
                tutorialName: obj.tutorial.name,
                tutorialUrl: obj.tutorial.url,
                code: obj.code,
                id: obj.id,
              };
            });
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching code. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
    },
    mounted() {
      this.fetchCode();
    },
  };
</script>
