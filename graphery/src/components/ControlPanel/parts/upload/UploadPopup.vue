<template>
  <q-dialog v-model="showDialog">
    <UploadCard style="min-width: 30vw;" />
  </q-dialog>
</template>

<script>
  export default {
    components: {
      UploadCard: () =>
        import('@/components/ControlPanel/parts/upload/UploadCard'),
    },
    model: {
      prop: 'showDialog',
      event: 'changeDialogStatus',
    },
    props: {
      showDialog: {
        type: Boolean,
        default: false,
      },
    },
    computed: {
      dialogModel: {
        set(d) {
          this.$emit('changeDialogStatus', d);
        },
        get() {
          return this.showDialog;
        },
      },
    },
  };
</script>
