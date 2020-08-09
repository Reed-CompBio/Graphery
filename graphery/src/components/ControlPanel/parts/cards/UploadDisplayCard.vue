<template>
  <q-card class="upload-card">
    <q-card-section>
      <div class="upload-image q-mx-auto q-mt-sm">
        <ImageDisplay
          :resource-link="resourceLink"
          @showUploadInfo="(url) => $emit('showUploadInfo', url)"
        />
      </div>
      <div class="q-mt-md" style="text-align: center;">
        <code style="word-wrap: break-word; "> {{ alias }}</code>
      </div>
    </q-card-section>
    <q-separator />
    <q-card-actions align="center">
      <UploadActionButton label="Relative Link" @click="copyRelativeUrl" />
    </q-card-actions>
  </q-card>
</template>

<script>
  import { saveTextToClipboard } from '@/services/helpers';

  export default {
    components: {
      ImageDisplay: () =>
        import('@/components/ControlPanel/parts/upload/ImageDisplay'),
      UploadActionButton: () =>
        import('@/components/ControlPanel/parts/buttons/UploadActionButton'),
    },
    props: {
      resourceLink: {
        type: String,
        default: '',
      },
      alias: {
        type: String,
        default: '',
      },
    },
    methods: {
      copyRelativeUrl() {
        saveTextToClipboard(this.resourceLink);
      },
    },
  };
</script>
