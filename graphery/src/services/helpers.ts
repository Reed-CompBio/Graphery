import { exportFile } from 'quasar';
import { copyToClipboard } from 'quasar';

export function toLocalDateString(locale: string, dateString: string) {
  return new Intl.DateTimeFormat(locale).format(new Date(dateString));
}

export const jpegMIMEType = 'image/jpeg';
export const jsonMIMEType = 'application/json';

export function saveTextToClipboard(text: string) {
  copyToClipboard(text)
    .then(() => {
      console.log('copied successfully');
    })
    .catch((err) => {
      console.error('Cannot copy result due to error:', err);
    });
}

export function saveToFile(
  fileName: string,
  rawData: string,
  mimeType: string
) {
  return exportFile(fileName, rawData, mimeType);
}
