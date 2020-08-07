<script>
  import { apiCaller } from '@/services/apis';
  import { deleteMutation } from '@/services/queries';
  import { errorDialog, successDialog } from '@/services/helpers';
  import { newModelUUID } from '@/services/params';

  export default {
    props: {
      message: {
        type: String,
      },
      id: {
        type: String,
        default: null,
      },
      contentType: {
        type: String,
      },
    },
    methods: {
      checkDelete() {
        if (!this.id || this.id === newModelUUID) {
          errorDialog({
            message: 'Cannot delete content since `id` is not specified.',
          });
          return false;
        }

        if (!this.contentType) {
          errorDialog({
            message:
              'Cannot delete content since `contentType` is not specified.',
          });
          return false;
        }

        return true;
      },
      showDeleteDialog() {
        this.$q
          .dialog({
            title: 'Confirm',
            message: this.message,
            cancel: true,
            persistent: true,
            noEscDismiss: true,
            noBackdropDismiss: true,
            focus: 'cancel',
          })
          .onOk(() => {
            this.postDelete();
          })
          .onCancel(() => null)
          .onDismiss(() => null);
      },
      postDelete() {
        if (!this.checkDelete()) {
          return;
        }
        apiCaller(deleteMutation, {
          contentType: this.contentType,
          id: this.id,
        })
          .then((data) => {
            if (!data.deleteContent.success) {
              throw Error('Unknown Reason.');
            } else {
              successDialog({
                message: 'Delete Successfully!',
              });
            }
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during deleting ${this.contentType} with id ${this.id}. ${err}`,
            });
          });
      },
    },
  };
</script>
