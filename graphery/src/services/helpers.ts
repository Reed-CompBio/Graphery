import { exportFile } from 'quasar';
import { copyToClipboard } from 'quasar';
import { apiCaller } from '@/services/apis';
import { userInfoQuery } from '@/services/queries';
import store from '@/store/index';
import { Notify } from 'quasar';
import { Location } from 'vue-router';
import router from '@/router/index';
import i18n from '@/i18n';

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

export function warningDialog(info: { message: string }) {
  Notify.create({
    ...info,
    type: 'warning',
    icon: 'report',
    multiLine: true,
    group: false,
    timeout: 10000,
    actions: [
      {
        label: 'Contact Dev',
        color: 'red',
        handler: () => {
          // TODO add a feedback page
          window.open('');
        },
      },
      {
        label: 'Close',
        color: 'red',
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
  const data = await apiCaller(userInfoQuery);
  action();
  if (data) {
    await store.dispatch('setUser', data['userInfo']);
  }
}

export function resolveLink(routerLinkObj: Location) {
  const { href } = router.resolve(routerLinkObj);
  return href;
}

export function resolveAndOpenLink(routerLinkObj: Location) {
  window.open(resolveLink(routerLinkObj), '_blank');
}

export function notAvailableMessage() {
  errorDialog({
    message: i18n.tc('tooltips.notAvailableCurrently'),
  });
}

export function rankToText(rank: { level: number; section: number }) {
  return `${
    rank.level < 10
      ? '00' + rank.level.toString()
      : rank.level < 100
      ? '0' + rank.level.toString()
      : rank.level.toString()
  }-${rank.section}`;
}
