import { exportFile } from 'quasar';
import { copyToClipboard } from 'quasar';
import { apiCaller } from '@/services/apis';
import { userInfoQuery } from '@/services/queries';
import store from '@/store/index';
import { Notify } from 'quasar';

export function successDialog(info: { message: string }) {
  Notify.create({
    ...info,
    type: 'positive',
    timeout: 1000,
    actions: [
      {
        label: 'Close',
        color: 'white',
        handler: () => null,
      },
    ],
  });
}

export function errorDialog(info: { message: string }) {
  Notify.create({
    ...info,
    type: 'negative',
    icon: 'report',
    multiLine: true,
    group: false,
    timeout: 10000,
    actions: [
      {
        label: 'Contact Dev',
        color: 'yellow',
        handler: () => {
          // TODO add a feedback page
          window.open('');
        },
      },
      {
        label: 'Close',
        color: 'yellow',
        handler: () => null,
      },
    ],
  });
}

export function toLocalDateString(locale: string, dateString: string) {
  return new Intl.DateTimeFormat(locale).format(new Date(dateString));
}

export const jpegMIMEType = 'image/jpeg';
export const jsonMIMEType = 'application/json';

export function saveTextToClipboard(text: string) {
  copyToClipboard(text)
    .then(() => {
      successDialog({ message: 'copied successfully' });
    })
    .catch((err) => {
      errorDialog({
        message: 'Cannot copy result due to ' + err,
      });
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
