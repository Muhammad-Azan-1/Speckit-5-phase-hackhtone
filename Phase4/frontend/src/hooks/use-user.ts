import useSWR, { useSWRConfig } from 'swr';
import { useAuth } from '@/hooks/use-auth';
import { getJWTToken } from '@/lib/auth-client';
import { toast } from 'sonner';

interface UserPreferences {
    theme: 'light' | 'dark';
    show_completed_tasks: boolean;
    date_format: string;
}

// SWR fetcher
const fetcher = async (url: string) => {
    const token = await getJWTToken();
    if (!token) throw new Error('No token found');

    const response = await fetch(url, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        throw new Error('Failed to fetch data');
    }

    return response.json();
};

export function useUserPreferences() {
    const { user } = useAuth();
    const { mutate } = useSWRConfig();
    const key = user?.id ? `${process.env.NEXT_PUBLIC_API_URL}/api/user/preferences` : null;

    const { data, error, isLoading } = useSWR<UserPreferences>(
        key,
        fetcher
    );

    const updatePreferences = async (newPrefs: UserPreferences) => {
        if (!user?.id) return;

        // Optimistic Update
        mutate(
            key,
            newPrefs,
            false
        );

        try {
            const token = await getJWTToken();
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/user/preferences`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newPrefs)
            });

            if (!response.ok) throw new Error('Failed');

            mutate(key); // Revalidate
            toast.success('Preferences saved successfully!');
            return true;
        } catch (error) {
            toast.error('Failed to update preferences');
            mutate(key); // Revert
            return false;
        }
    };

    return {
        preferences: data || {
            theme: 'light',
            show_completed_tasks: true,
            date_format: 'MM/DD/YYYY'
        },
        isLoading,
        isError: error,
        updatePreferences
    };
}
