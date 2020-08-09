import { deleteImage, uploadStatic } from '@/services/queries';
import { apiCaller } from '@/services/apis';
import { errorDialog, successDialog } from '@/services/helpers';

export function fileUploadAction(files: [File]) {
  const form = new FormData();
  form.append('query', uploadStatic);
  for (const file of files) {
    form.append(file.name, file);
  }

  return apiCaller(null, null, form).then((data) => {
    if (!data || !('uploadStatic' in data)) {
      throw Error('Invalid data returned.');
    }

    if (!data.uploadStatic.success) {
      throw Error('Uploading image is failed.');
    }

    successDialog({
      message: 'Upload Image Successfully!',
    });
  });
}

export function imgDelCallback(filename: string) {
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
}
