import { exportFile } from 'quasar';
import { copyToClipboard } from 'quasar';

export function toLocalDateString(locale: string, dateString: string) {
  return new Intl.DateTimeFormat(locale).format(new Date(dateString));
}

export const pngMIMEType = 'image/png';

export function saveTextToClipboard(text: string) {
  copyToClipboard(text)
    .then(() => {
      console.log('copied successfully');
    })
    .catch((err) => {
      console.error('Cannot copy result due to error:', err);
    });
}

export function saveToPngFile(fileName: string, rawData: string) {
  const byteCharacters = atob(rawData.split(',')[1]);

  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }

  const byteArray = new Uint8Array(byteNumbers);
  return exportFile(fileName, byteArray, pngMIMEType);
}
