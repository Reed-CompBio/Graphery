import { exportFile } from 'quasar';
import { copyToClipboard } from 'quasar';
import { apiCaller } from '@/services/apis';
import { userInfoQuery } from '@/services/queries';
import store from '@/store/index';

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

export async function pullUser(
  action: () => void = () => {
    return null;
  }
) {
  const [data, errors] = await apiCaller(userInfoQuery);
  action();
  if (!errors && data) {
    await store.dispatch('setUser', data['userInfo']);
  }
}
