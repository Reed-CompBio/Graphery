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
            <UploadDisplayCard
              :resource-link="props.row.relativeUrl"
              @showUploadInfo="showUploadInfo"
            />
          </div>
        </template>
      </q-table>
      <UploadInfoWindow
        :resource-link="infoWindowIntel"
        v-model="showUploadInfoWindow"
      />
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import loadingMixin from '../mixins/LoadingMixin';
  import UploadDisplayCard from '@/components/ControlPanel/parts/cards/UploadDisplayCard';
  import { apiCaller } from '@/services/apis';
  import { fetchUploads } from '@/services/queries';
  import { errorDialog } from '@/services/helpers';
  import UploadInfoWindow from '@/components/ControlPanel/editors/UploadInfoWindow';

  export default {
    mixins: [loadingMixin],
    components: {
      UploadInfoWindow,
      UploadDisplayCard,
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame'),
    },
    data() {
      return {
        columns: [
          {
            name: 'relativeUrl',
            label: 'relativeUrl',
            field: 'relativeUrl',
          },
          {
            name: 'id',
            label: 'id',
            field: 'id',
            required: true,
          },
        ],
        pagination: {
          sortBy: '',
          rowsPerPage: 20,
        },
        tableContent: [],
        showUploadInfoWindow: false,
        infoWindowIntel: '',
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
      showInfo() {
        this.showUploadInfoWindow = true;
      },
      changeInfoWindowIntel(url) {
        this.infoWindowIntel = url;
      },
      showUploadInfo(url) {
        this.changeInfoWindowIntel(url);
        this.showInfo();
      },
    },
    mounted() {
      this.fetchUploadsContent();
    },
  };
</script>
