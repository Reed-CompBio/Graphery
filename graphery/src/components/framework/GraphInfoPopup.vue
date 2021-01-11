<template>
  <q-dialog
    v-model="popupModel"
    :auto-close="false"
    transition-show="flip-down"
    transition-hide="flip-up"
  >
    <q-card style="width: 40%">
      <q-bar>
        Graph Abstract
        <q-space />
        <q-toggle v-model="showAbstractToggle" />
        <q-btn flat dense icon="close" @click="closePopup" />
      </q-bar>
      <q-card-section style="max-height: 60vh" class="scroll">
        <MarkdownSection
          class="q-mx-md"
          :markdown-raw="graphAbstractMarkdown"
        />
      </q-card-section>
      <q-separator />
      <q-card-actions align="center" class="q-my-sm">
        <q-btn type="" :label="$t('Close')" @click="closePopup" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
  import MarkdownSection from '@/components/framework/md/MarkdownSection';
  import { successDialog } from '@/services/helpers';
  export default {
    components: { MarkdownSection },
    props: {
      graphAbstractMarkdown: {
        type: String,
        default: '',
      },
      dialogModel: {
        type: Boolean,
      },
    },
    model: {
      prop: 'dialogModel',
      model: 'dialogModelChange',
      // don't know why this doesn't work
    },
    computed: {
      popupModel: {
        set(d) {
          this.$emit('dialogModelChange', d);
        },
        get() {
          return this.dialogModel;
        },
      },
      showAbstractToggle: {
        set(d) {
          this.$store.commit('settings/CHANGE_GRAPH_ABSTRACT_POPUP_SHOW', d);
          successDialog(
            {
              message: this.$t('You can also edit this in the Settings page.'),
            },
            3000
          );
        },
        get() {
          return this.$store.getters['settings/graphAbstractPopupShow'];
        },
      },
    },
    methods: {
      closePopup() {
        this.popupModel = false;
      },
    },
  };
</script>
