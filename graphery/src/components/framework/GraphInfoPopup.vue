<template>
  <q-dialog
    v-model="dialogModel"
    :auto-close="false"
    transition-show="flip-down"
    transition-hide="flip-up"
  >
    <q-card style="width: 40%">
      <q-bar>
        Graph Abstract
        <q-space />
        <q-btn flat dense icon="close" />
      </q-bar>
      <q-card-section style="max-height: 60vh" class="scroll">
        <MarkdownSection
          class="q-mx-md"
          :markdown-raw="graphAbstractMarkdown"
        />
      </q-card-section>
      <q-separator />
      <q-card-actions align="center" class="q-my-sm">
        <q-btn type="" label="Got Ya!" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
  import MarkdownSection from '@/components/framework/md/MarkdownSection';
  export default {
    components: { MarkdownSection },
    props: {
      graphAbstractMarkdown: {
        type: String,
        default: '',
      },
      dialogModel: {
        type: Boolean,
        default: false,
      },
    },
    model: {
      prop: 'dialogModel',
      model: 'dialogChange',
    },
    computed: {
      model: {
        set(d) {
          this.$emit('dialogChange', d);
        },
        get() {
          return this.dialogModel;
        },
      },
    },
  };
</script>
