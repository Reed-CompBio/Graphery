<template>
  <q-dialog v-model="displayModel">
    <q-card style="height: 80vh; min-width: 60vw;">
      <q-bar>
        <div id="picture-title-section">
          {{ $t('article.Figure') }}
        </div>
        <q-space />
        <div id="action-section">
          <q-btn
            flat
            dense
            class="figure-action-btn"
            icon="mdi-magnify-plus-outline"
            @click="zoomIn"
          />
          <q-btn
            flat
            dense
            class="figure-action-btn"
            icon="mdi-magnify-minus-outline"
            @click="zoomOut"
          />
        </div>
        <q-space />
        <div id="picture-close-section">
          <q-btn
            flat
            dense
            icon="close"
            @click="
              () => {
                this.displayModel = false;
              }
            "
          />
        </div>
      </q-bar>
      <v-zoomer-gallery
        ref="zoomer"
        id="picture-zoomer-gallery"
        pivot="cursor"
        doubleClickToZoom
        mouseWheelToZoom
        :list="displayedList"
        v-model="displayedIndex"
      />
    </q-card>
  </q-dialog>
</template>

<script>
  import Vue from 'vue';
  import VueZoomer from 'vue-zoomer';
  Vue.use(VueZoomer);

  export default {
    props: {
      photoList: {
        type: Array,
        default: null,
      },
      photoIndex: {
        type: Number,
        default: 0,
      },
      display: {
        type: Boolean,
        default: true,
      },
    },
    computed: {
      displayedList() {
        return this.photoList;
      },
      displayedIndex: {
        set(d) {
          this.$emit('pictureIndexUpdate', d);
        },
        get() {
          return this.photoIndex;
        },
      },
      displayModel: {
        set(d) {
          this.$emit('pictureDisplayChange', d);
        },
        get() {
          return this.display;
        },
      },
    },
    methods: {
      zoomIn() {
        this.$refs.zoomer.zoomIn();
      },
      zoomOut() {
        this.$refs.zoomer.zoomOut();
      },
    },
  };
</script>

<style lang="sass" scoped>
  .figure-action-btn
    margin: 0.02rem 0.3rem

  .vue-zoomer-gallery
    cursor: move !important

  #picture-zoomer-gallery
    width: 100%
    height: 100%
</style>
