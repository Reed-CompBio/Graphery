<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Uploads
    </template>
    <template>
      <q-table
        :data="tableContent"
        :columns="columns"
        :pagination="pagination"
        row-key="name"
        grid
        hide-header
        :loading="loadingContent"
      >
        <template v-slot:item="props">
          <div class="q-pa-xs col-xs-12 col-sm-4 col-md-3 col-lg-2">
            <UploadDisplayCard :resource-link="props.row.file" />
          </div>
        </template>
      </q-table>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin';
  import UploadDisplayCard from '@/components/ControlPanel/parts/cards/UploadDisplayCard';
  import { apiCaller } from '@/services/apis';
  import { fetchUploads } from '@/services/queries';
  import { errorDialog } from '@/services/helpers';

  export default {
    mixins: [loadingMixin],
    components: {
      UploadDisplayCard,
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame'),
    },
    data() {
      return {
        columns: [
          {
            name: 'file',
            label: 'File',
            field: 'file',
          },
          {
            name: 'id',
            label: 'id',
            field: 'id',
          },
        ],
        pagination: {
          sortBy: '',
          rowsPerPage: 10,
        },
        tableContent: [],
      };
    },
    methods: {
      fetchUploadsContent() {
        this.startLoading();
        apiCaller(fetchUploads)
          .then((data) => {
            if (!data || !('allUploads' in data)) {
              throw Error('Invalid data returned.');
            }

            this.tableContent = data.allUploads;
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching uploads. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
    },
    mounted() {
      this.fetchUploadsContent();
    },
  };
</script>
