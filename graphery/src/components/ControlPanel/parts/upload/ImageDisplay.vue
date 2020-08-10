<template>
  <q-img :src="imageSrc" style="min-height: 150px; min-width: 150px">
    <template v-slot:error>
      <div class="absolute-full flex flex-center bg-negative text-white">
        Cannot load image
      </div>
    </template>
    <!-- TODO use on hover -->
    <q-chip clickable dense size="sm" @click="$emit('showUploadInfo')">
      <q-icon name="info" size="sm" color="white" />
    </q-chip>
  </q-img>
</template>

<script>
  import mime from 'mime-types';
  import videoPlaceholder from '@/assets/icons/video.svg';
  import filePlaceholder from '@/assets/icons/file.svg';

  export default {
    props: {
      resourceLink: {
        type: String,
        default: '',
      },
      showVideo: {
        type: Boolean,
        default: false,
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
  };
</script>
