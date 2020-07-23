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
        :loading="loadingCategories"
        no-data-label="No Categories are found."
        row-key="id"
        separator="cell"
        class="custom-table"
      >
        <template v-slot:top>
          <q-btn
            icon="refresh"
            @click.prevent="fetchCategories"
            label="Refresh"
          ></q-btn>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td key="category" :props="props">
              <q-btn :label="props.row.category" flat>
                <SwitchTooltip text="Open In Editor"></SwitchTooltip>
              </q-btn>
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
  import { apiCaller } from '../../services/apis';
  import { categoryQuery } from '../../services/queries';
  import { errorDialog } from '../../services/helpers';

  export default {
    components: {
      SwitchTooltip: () => import('../framework/SwitchTooltip'),
      ControlPanelContentFrame: () => import('./ControlPanelContentFrame.vue'),
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
      startLoading() {
        this.loadingCategories = true;
      },
      finishedLoading() {
        this.loadingCategories = false;
      },
      fetchCategories() {
        this.startLoading();

        apiCaller(categoryQuery)
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
