<script>
  import { deleteImage, uploadImage } from '@/services/queries';
  import { apiCaller } from '@/services/apis';
  import { errorDialog, successDialog } from '@/services/helpers';

  export default {
    methods: {
      fileUploadAction(fileName, files) {
        // TODO post lang with axios
        const form = new FormData();
        form.append('query', uploadImage);
        for (const file of files) {
          form.append(this.anchorId, file);
        }

        apiCaller(null, null, form)
          .then((data) => {
            if (!data || !('uploadStatic' in data)) {
              throw Error('Invalid data returned.');
            }

            if (!data.uploadStatic.success) {
              throw Error('Uploading image is failed.');
            }

            this.$refs.mdEditor.replaceUrl(fileName, data.uploadStatic.url);
            successDialog({
              message: 'Upload Image Successfully!',
            });
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during upload image. ${err}`,
            });
          });
      },
      imgDelCallback([filename]) {
        apiCaller(deleteImage, {
          url: filename,
        })
          .then((data) => {
            if (!data || !('deleteStatic' in data)) {
              throw Error('Invalid data returned');
            }

            if (!data.deleteStatic.success) {
              throw Error(`Deleting ${filename} is failed.`);
            }

            successDialog({
              message: 'Delete Image Successfully!',
            });
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during deleting uploaded image. ${err}`,
            });
          });
      },
    },
  };
</script>
