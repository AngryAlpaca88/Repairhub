import { useQuery } from '@tanstack/react-query';
import { api } from '../api';
import { tokenStore } from '../auth/tokenStore';

interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  company_id: number;
  is_active: boolean;
  locations: Array<{
    id: number;
    name: string;
  }>;
}

export function useCurrentUser() {
  const hasToken = tokenStore.hasToken();

  const { data: user, isLoading, error } = useQuery<User>({
    queryKey: ['currentUser'],
    queryFn: () => api.get('/auth/me'),
    enabled: hasToken,
    retry: false,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  return {
    user: hasToken ? user : null,
    isLoading: hasToken ? isLoading : false,
    error,
    isAuthenticated: !!user,
  };
}
