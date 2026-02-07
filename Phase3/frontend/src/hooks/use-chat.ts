import useSWR, { useSWRConfig } from 'swr';
import { useAuth } from '@/hooks/use-auth';
import { getJWTToken } from '@/lib/auth-client';
import { Message, Conversation } from '@/types/chat';

// Shared fetcher
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

export function useConversations() {
    const { user } = useAuth();

    // Fetch conversations only when user is logged in
    const { data, error, isLoading, mutate } = useSWR<Conversation[]>(
        user?.id ? `${process.env.NEXT_PUBLIC_API_URL}/chat/conversations` : null,
        fetcher,
        {
            revalidateOnFocus: false, // Don't re-fetch every time window gets focus
            dedupingInterval: 60000, // Cache for 1 minute
        }
    );

    return {
        conversations: data || [],
        isLoading,
        isError: error,
        mutate,
    };
}

export function useMessages(conversationId: number | null) {
    const { user } = useAuth();

    const { data, error, isLoading, mutate } = useSWR<Message[]>(
        user?.id && conversationId ? `${process.env.NEXT_PUBLIC_API_URL}/chat/conversations/${conversationId}/messages` : null,
        fetcher,
        {
            revalidateOnFocus: false,
            dedupingInterval: 60000,
        }
    );

    return {
        messages: data || [],
        isLoading,
        isError: error,
        mutate,
    };
}
