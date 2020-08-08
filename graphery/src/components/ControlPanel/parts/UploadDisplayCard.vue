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
          <q-chip clickable dense size="sm">
            <q-icon name="info" size="sm" color="white" />
          </q-chip>
        </q-img>
      </div>
      <div class="q-mt-sm img-caption">
        <code>
          {{ resourceLink }}
        </code>
      </div>
    </q-card-section>
    <q-separator />
    <q-card-actions align="center">
      <q-btn flat label="Relative Link" />
    </q-card-actions>
  </q-card>
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

<style lang="sass">
  .img-caption
    text-align: center
    word-wrap: break-word
    font-size: 85%
    background-color: rgba(27,31,35,.05)
    border-radius: 3px
    font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace
</style>
