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

interface ITokenStore {
  accessToken?: string;
}

export const useAuthStore = defineStore('auth', {
  state: (): ITokenStore => {
    const appConfig = useAppConfig();
    return {
      accessToken: getCookie(appConfig.cookieKeys.accessToken) || undefined,
    };
  },
  getters: { loggedIn: ({ accessToken }): boolean => !!accessToken },
  actions: {
    logIn(token: string, redirect: boolean = true) {
      this.accessToken = token;
      const appConfig = useAppConfig();
      setCookie(appConfig.cookieKeys.accessToken, this.accessToken);
      if (redirect)
        navigateTo(
          (useRoute().query.redirect as string) || appConfig.pages.home.path
        );
    },
    logOut(options?: { redirect?: string }): void {
      const appConfig = useAppConfig();
      removeCookie(appConfig.cookieKeys.accessToken);
      this.accessToken = undefined;
      if (options && options.redirect)
        navigateTo({
          path: appConfig.pages.login.path,
          query: { redirect: options.redirect },
        });
      else navigateTo(appConfig.pages.login.path);
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}
