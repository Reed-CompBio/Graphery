<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Categories
    </template>
    <template>
      <q-table
        :data="tableContent"
        :columns="columns"
        :pagination="pagination"
        :loading="loadingTable"
        no-data-label="No Categories are found."
        row-key="id"
        separator="cell"
        class="custom-table"
      >
        <template v-slot:top>
          <RefreshButton :fetch-func="fetchCategories" />
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td key="category" :props="props">
              <OpenInEditorButton :label="props.row.category" />
            </q-td>

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
  import { categoryListQuery } from '../../../services/queries';
  import { errorDialog } from '../../../services/helpers';
  import loadingMixin from './LoadingMixin.vue';

  export default {
    mixins: [loadingMixin],
    components: {
      ControlPanelContentFrame: () => import('../ControlPanelContentFrame.vue'),
      RefreshButton: () => import('../parts/RefreshButton.vue'),
      OpenInEditorButton: () => import('../parts/OpenInEditorButton.vue'),
    },
    data() {
      return {
        columns: [
          {
            name: 'category',
            label: 'Category',
            field: 'category',
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
            name: 'id',
            label: 'ID',
            field: 'id',
            align: 'center',
            required: true,
          },
        ],
        pagination: {
          sortBy: 'category',
          rowsPerPage: 20,
        },
        loadingCategories: false,
        tableContent: [],
      };
    },
    methods: {
      fetchCategories() {
        this.startLoading();

        apiCaller(categoryListQuery)
          .then(([data, errors]) => {
            if (errors) {
              throw Error(errors);
            }

            if (!data || !('allCategories' in data)) {
              throw Error('Invalid Result is received.');
            }

            this.tableContent = data['allCategories'];
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching categories. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
    },
    mounted() {
      this.fetchCategories();
    },
  };
</script>
