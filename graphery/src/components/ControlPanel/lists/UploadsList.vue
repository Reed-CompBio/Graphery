<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Uploads
    </template>
    <template>
      <UploadTable @showUploadInfo="showUploadInfo" />
      <UploadInfoPopup
        :resource-link="infoWindowIntel"
        v-model="showUploadInfoWindow"
      />
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  export default {
    components: {
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
    },
  };
</script>
