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
      <UploadActionButton label="Relative Link" />
    </q-card-actions>
  </q-card>
</template>

<script>
  import mime from 'mime-types';
  import videoPlaceholder from '@/assets/icons/video.svg';
  import filePlaceholder from '@/assets/icons/file.svg';
  import { BASE_URL } from '@/services/api_entry';
  import UploadActionButton from '@/components/ControlPanel/parts/buttons/UploadActionButton';

  export default {
    components: { UploadActionButton },
    props: {
      resourceLink: {
        type: String,
        default: '',
      },
    },
    computed: {
      correctedLink() {
        if (
          // if it's not relative/absolute url, make it relative url
          this.resourceLink.startsWith(BASE_URL) ||
          this.resourceLink.startsWith('/')
        ) {
          return this.resourceLink;
        } else {
          return '/' + this.resourceLink;
        }
      },
      lookUpResult() {
        return mime.lookup(this.correctedLink);
      },
      isImage() {
        return this.lookUpResult && this.lookUpResult.startsWith('image');
      },
      isVideo() {
        return this.lookUpResult && this.lookUpResult.startsWith('video');
      },
      imageSrc() {
        return this.isImage
          ? this.correctedLink
          : this.isVideo
          ? videoPlaceholder
          : filePlaceholder;
      },
    },
    methods: {
      testFunc() {
        console.log('test');
      },
    },
  };
</script>
