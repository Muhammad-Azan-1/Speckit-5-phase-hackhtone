import { useSession } from '@/lib/auth-client';
import { useRouter } from 'next/navigation';

export function useAuth() {
  const router = useRouter();
  const { data: session, isPending, error } = useSession();

  const user = session?.user || null;
  const isAuthenticated = !!user;

  // Helper to ensure token is in localStorage (for FastAPI calls)
  // This is a safety check/sync, though login form handles setting it.
  if (session?.session?.token && typeof window !== 'undefined') {
    // Note: Better Auth session token != JWT token for FastAPI
    // We rely on login-form to set the JWT token in 'auth-token'
  }

  const logout = async () => {
    const { signOut } = await import('@/lib/auth-client');
    await signOut();
    localStorage.removeItem('auth-token');
    router.push('/login');
  };

  return {
    user,
    loading: isPending,
    error,
    isAuthenticated,
    logout,
    // login/register are handled by specific forms now, so we don't export them here
    // to encourage using the Better Auth client directly
  };
}