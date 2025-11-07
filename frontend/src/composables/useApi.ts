export const useApi = () => {
  const { $http } = useNuxtApp();
  const config = useRuntimeConfig();
  const API_BASE = config.public.apiBase;

  return {
    auth: {
      login: (body: LoginRequest) =>
        $http<LoginResponse>('/auth/login', { method: 'POST', body }),
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
      detail: (id: string) => $http<Dataset>(`/datasets/${id}`),
      viewData: (id: string) =>
        $http(`/datasets/${id}/view`, {
          method: 'POST',
        }),
      download: (id: string) =>
        $http.raw(`/datasets/${id}/download`, {
          method: 'GET',
        }),
    },
  };
};
