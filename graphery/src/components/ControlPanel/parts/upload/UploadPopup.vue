<template>
  <q-dialog v-model="dialogModel">
    <UploadCard style="min-width: 30vw;" :finalCallback="finalCallback" />
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
      finalCallback: {
        type: Function,
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
