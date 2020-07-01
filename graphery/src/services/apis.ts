import axios, { AxiosInstance, AxiosResponse } from 'axios';
import vuex from '../store/index';

const PRO_BASE_URL = 'http://localhost:8082';
const DEV_BASE_URL = 'http://localhost:8082';
const BASE_URL =
  process.env.NODE_ENV === 'production' ? PRO_BASE_URL : DEV_BASE_URL;

export const apiClient: AxiosInstance = axios.create({
  withCredentials: true,
  baseURL: BASE_URL,
});

export async function apiCaller(
  query: string,
  variables: object | null = null
) {
  if (vuex.state.csrfToken === null) {
    const token = await apiClient.get('/csrf').then((re) => {
      return re.data.csrfToken;
    });
    vuex.commit('SET_CSRF_TOKEN', token);
  }
  const response = await apiClient.post(
    '/graphql',
    {
      query,
      variables,
    },
    {
      headers: {
        'X-CSRFToken': vuex.state.csrfToken,
      },
    }
  );

  return [response.data.data, response.data.errors];
}
