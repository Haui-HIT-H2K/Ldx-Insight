/**
 * Copyright 2025 Haui.HIT - H2K
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

const API_REQUEST_TIMEOUT = 20000; // 20s
const headers = { 'App-Code': 'hit-members' };
export default defineNuxtPlugin(() => {
  const runtimeConfig = useRuntimeConfig();
  const authStore = useAuthStore();

  const $http = $fetch.create({
    baseURL: `${runtimeConfig.public.apiBase}`,
    headers,
    timeout: API_REQUEST_TIMEOUT,
    onRequest({ options }) {
      const token = authStore.accessToken;
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${token}`,
      };
    },

    async onResponseError({ response, request }) {
      if (response.status === 401) {
        if (!request.toString().includes('/auth')) {
          try {
            const config = useRuntimeConfig();
            const { data } = await $fetch<LoginResponse>(
              `${config.public.apiBase}/api/v1/auth/refresh`,
              {
                method: 'POST',
                body: { refreshToken: authStore.refreshToken },
              }
            );

            authStore.logIn(data, false);
            await refreshNuxtData();
          } catch {
            console.error(response._data);
            authStore.logOut();
            throw new Error('Token refresh failed');
          }
        } else {
          console.error(response._data);
          authStore.logOut({
            redirect: (useRoute().query.redirect as string) || '/',
          });
        }
      }
    },
  });

  return {
    provide: { http: $http },
  };
});
