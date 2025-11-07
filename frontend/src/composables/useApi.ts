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

export const useApi = () => {
  const { $http } = useNuxtApp();
  const config = useRuntimeConfig();
  const API_BASE = config.public.apiBase;

  return {
    auth: {
      login: (body: LoginRequest) =>
        $http<AuthResponse>(`${API_BASE}/auth/login`, {
          method: 'POST',
          body,
        }),
      register: (body: LoginRequest) =>
        $http<AuthResponse>(`${API_BASE}/auth/register`, {
          method: 'POST',
          body,
        }),
    },
    stats: {
      summary: () => {
        return $http<SummaryStats>(`${API_BASE}/stats/summary`);
      },
      topViewed: (limit?: number) => {
        return $http<Dataset[]>(`${API_BASE}/stats/top-viewed`, {
          query: { limit },
        });
      },
      topDownloaded: (limit?: number) => {
        return $http<Dataset[]>(`${API_BASE}/stats/top-downloaded`, {
          query: { limit },
        });
      },
      byCategory: () => {
        return $http<CategoryStat[]>(`${API_BASE}/stats/by-category`);
      },
    },

    dataset: {
      category: () => {
        return $http<string[]>(`${API_BASE}/datasets/categories`);
      },
      list: (params?: DatasetRequestParams) =>
        $http<DatasetResponse>(`${API_BASE}/datasets`, {
          query: params,
        }),
      detail: (id: string) => $http<Dataset>(`${API_BASE}/datasets/${id}`),
      viewData: (id: string) =>
        $http(`${API_BASE}/datasets/${id}/view`, {
          method: 'POST',
        }),
      download: (id: string) =>
        $http(`${API_BASE}/datasets/${id}/download`, {
          method: 'GET',
        }),
      downloadFile: (id: string) =>
        $http.raw(`${API_BASE}/datasets/${id}/download.csv`, {
          method: 'GET',
          responseType: 'blob',
        }),
    },
  };
};
