import axios, { AxiosInstance, AxiosResponse } from 'axios';

const PRO_BASE_URL = 'http://localhost:8082';
const DEV_BASE_URL = 'http://localhost:8082';
const BASE_URL =
  process.env.NODE_ENV === 'production' ? PRO_BASE_URL : DEV_BASE_URL;

export const apiClient: AxiosInstance = axios.create({
  withCredentials: true,
  baseURL: BASE_URL,
});

export function apiCallWrapper(
  query: string,
  variables: object | null = null,
  callback: (response: AxiosResponse) => null
) {
  apiClient
    .get('/csrf')
    .then((re) => {
      return re.data.csrfToken;
    })
    .then((csrfToken) => {
      apiClient
        .post(
          '/graphql',
          {
            query,
            variables,
          },
          {
            headers: {
              'X-CSRFToken': csrfToken,
            },
          }
        )
        .then((re) => {
          callback(re);
        })
        .catch((err) => {
          console.error(err);
        });
    })
    .catch((err) => {
      console.error(err);
    });
}
