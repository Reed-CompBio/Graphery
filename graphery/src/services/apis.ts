import axios, { AxiosInstance } from 'axios';
import vuex from '../store/index';
import { BASE_URL } from '@/services/api_entry';

export const apiClient: AxiosInstance = axios.create({
  withCredentials: true,
  baseURL: BASE_URL,
});

export function getCookie(name: string) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrfTokenCookieName = 'csrftoken';

export async function apiCaller(
  query: string,
  variables: object | null = null
) {
  if (vuex.state.csrfToken === null) {
    // TODO use vuex. add a renew token in login page.
    await apiClient.get('/csrf');
  }
  const response = await apiClient.post(
    '/graphql',
    {
      query,
      variables,
    },
    {
      headers: {
        // TODO corresponding, change this
        'X-CSRFToken': getCookie(csrfTokenCookieName),
      },
    }
  );

  return [response.data.data, response.data.errors];
}
