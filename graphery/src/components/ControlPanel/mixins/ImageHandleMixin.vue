<script>
  import { deleteImage, uploadImage } from '@/services/queries';
  import { apiCaller } from '@/services/apis';
  import { errorDialog, successDialog } from '@/services/helpers';

  export default {
    methods: {
      imgAddCallback(fileName, file) {
        // TODO post lang with axios
        const form = new FormData();
        form.append('query', uploadImage);
        form.append(this.anchorId, file);

        apiCaller(null, null, form)
          .then((data) => {
            if (!data || !('uploadStatics' in data)) {
              throw Error('Invalid data returned.');
            }

            if (!data.uploadStatics.success) {
              throw Error('Uploading image is failed.');
            }

            this.$refs.mdEditor.replaceUrl(fileName, data.uploadStatics.url);
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
            if (!data || !('deleteStatics' in data)) {
              throw Error('Invalid data returned');
            }

            if (!data.deleteStatics.success) {
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
