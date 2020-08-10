<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Uploads
    </template>
    <template>
      <UploadTable
        ref="contentTable"
        @showUploadInfo="showUploadInfo"
        @startUpload="startUpload"
      />
      <UploadInfoPopup
        :resource-link="infoWindowIntel.url"
        :id="infoWindowIntel.id"
        content-type="UPLOADS"
        v-model="showUploadInfoWindow"
        :finalCallback="refreshContent"
      />
      <UploadPopup v-model="showUploadPopup" :finalCallback="refreshContent" />
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  export default {
    components: {
      UploadPopup: () =>
        import('@/components/ControlPanel/parts/upload/UploadPopup'),
      UploadTable: () =>
        import('@/components/ControlPanel/parts/upload/UploadTable'),
      UploadInfoPopup: () =>
        import('@/components/ControlPanel/parts/upload/UploadInfoPopup'),
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame'),
    },
    data() {
      return {
        showUploadInfoWindow: false,
        showUploadPopup: false,
        infoWindowIntel: '',
      };
    },
    methods: {
      showInfo() {
        this.showUploadInfoWindow = true;
      },
      showUploadInfo(obj) {
        this.infoWindowIntel = obj;
        this.showInfo();
      },
      startUpload() {
        this.showUploadPopup = true;
      },
      refreshContent() {
        this.$refs.contentTable.fetchUploadsContent();
      },
    },
  };
</script>
