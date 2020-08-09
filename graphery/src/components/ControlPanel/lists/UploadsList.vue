<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Uploads
    </template>
    <template>
      <UploadTable
        @showUploadInfo="showUploadInfo"
        @startUpload="startUpload"
      />
      <UploadInfoPopup
        :resource-link="infoWindowIntel"
        v-model="showUploadInfoWindow"
      />
      <UploadPopup v-model="showUploadPopup" />
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
      changeInfoWindowIntel(url) {
        this.infoWindowIntel = url;
      },
      showUploadInfo(url) {
        this.changeInfoWindowIntel(url);
        this.showInfo();
      },
      startUpload() {
        this.showUploadPopup = true;
      },
    },
  };
</script>
