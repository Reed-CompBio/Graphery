<template>
  <q-card class="upload-card">
    <q-card-section>
      <div class="upload-image q-mx-auto q-mt-sm">
        <q-img :src="imageSrc">
          <template v-slot:error>
            <div class="absolute-full flex flex-center bg-negative text-white">
              Cannot load image
            </div>
          </template>
          <!-- TODO use on hover -->
          <q-chip
            clickable
            dense
            size="sm"
            @click="$emit('showUploadInfo', this.resourceLink)"
          >
            <q-icon name="info" size="sm" color="white" />
          </q-chip>
        </q-img>
      </div>
    </q-card-section>
    <q-separator />
    <q-card-actions align="center">
      <UploadActionButton label="Relative Link" @click="copyRelativeUrl" />
    </q-card-actions>
  </q-card>
</template>

<script>
  import mime from 'mime-types';
  import videoPlaceholder from '@/assets/icons/video.svg';
  import filePlaceholder from '@/assets/icons/file.svg';
  import UploadActionButton from '@/components/ControlPanel/parts/buttons/UploadActionButton';
  import { saveTextToClipboard } from '@/services/helpers';

  export default {
    components: { UploadActionButton },
    props: {
      resourceLink: {
        type: String,
        default: '',
      },
    },
    computed: {
      lookUpResult() {
        return mime.lookup(this.resourceLink);
      },
      isImage() {
        return this.lookUpResult && this.lookUpResult.startsWith('image');
      },
      isVideo() {
        return this.lookUpResult && this.lookUpResult.startsWith('video');
      },
      imageSrc() {
        return this.isImage
          ? this.resourceLink
          : this.isVideo
          ? videoPlaceholder
          : filePlaceholder;
      },
    },
    methods: {
      copyRelativeUrl() {
        saveTextToClipboard(this.resourceLink);
      },
    },
  };
</script>
