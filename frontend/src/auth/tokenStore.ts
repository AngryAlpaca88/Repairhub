const TOKEN_KEY = 'repairhub_access_token';

export const tokenStore = {
  getToken: (): string | null => {
    if (typeof window === 'undefined') {
      return null;
    }
    return localStorage.getItem(TOKEN_KEY);
  },

  setToken: (token: string): void => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(TOKEN_KEY, token);
    }
  },

  clearToken: (): void => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(TOKEN_KEY);
    }
  },

  hasToken: (): boolean => {
    return !!tokenStore.getToken();
  },
};
