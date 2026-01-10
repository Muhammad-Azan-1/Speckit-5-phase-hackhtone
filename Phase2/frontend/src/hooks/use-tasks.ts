import useSWR, { useSWRConfig } from 'swr';
import { useAuth } from '@/hooks/use-auth';
import { getJWTToken } from '@/lib/auth-client';
import { Task } from '@/types/task';
import { toast } from 'sonner';

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
        throw new Error('Failed to fetch data.');
    }

    return response.json();
};

export function useTasks() {
    const { user } = useAuth();

    const { data, error, isLoading, mutate } = useSWR<Task[]>(
        user?.id ? `${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/tasks` : null,
        fetcher
    );

    return {
        tasks: data || [],
        isLoading,
        isError: error,
        mutate,
    };
}

export function useTodayTasks(limit: number = 5) {
    const { user } = useAuth();

    const { data, error, isLoading, mutate } = useSWR<{ tasks: Task[], count: number }>(
        user?.id ? `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/today?limit=${limit}` : null,
        fetcher
    );

    return {
        tasks: data?.tasks || [],
        count: data?.count || 0,
        isLoading,
        isError: error,
        mutate,
    };
}

export function useStats() {
    const { user } = useAuth();

    const { data, error, isLoading, mutate } = useSWR<{ total: number, completed: number, pending: number }>(
        user?.id ? `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/stats` : null,
        fetcher
    );

    return {
        stats: data || { total: 0, completed: 0, pending: 0 },
        isLoading,
        isError: error,
        mutate,
    };
}

export function useCategories() {
    const { user } = useAuth();

    const { data, error, isLoading, mutate } = useSWR<any[]>(
        user?.id ? `${process.env.NEXT_PUBLIC_API_URL}/api/categories` : null,
        fetcher
    );

    return {
        categories: data || [],
        isLoading,
        isError: error,
        mutate,
    };
}

export function useCategoryStats() {
    const { user } = useAuth();

    const { data, error, isLoading, mutate } = useSWR<any[]>(
        user?.id ? `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/stats/categories` : null,
        fetcher
    );

    return {
        categoryStats: data || [],
        isLoading,
        isError: error,
        mutate,
    };
}

// Hook for muting multiple keys
export function useTaskMutations() {
    const { mutate } = useSWRConfig();
    const { user } = useAuth();

    const refreshAll = () => {
        if (!user?.id) return;
        mutate(`${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/tasks`);
        mutate(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/stats`);
        mutate(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/today?limit=5`);
        mutate(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/stats/categories`);
    };

    const updateTaskCompletion = async (taskId: number, completed: boolean) => {
        if (!user?.id) return;

        // 1. Update Tasks List Optimistically
        mutate(
            `${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/tasks`,
            (currentTasks: Task[] | undefined) => {
                if (!currentTasks) return [];
                return currentTasks.map(t => t.id === taskId ? { ...t, completed } : t);
            },
            false
        );

        // 2. Update Stats Optimistically
        mutate(
            `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/stats`,
            (currentStats: any) => {
                if (!currentStats) return { total: 0, completed: 0, pending: 0 };
                return {
                    ...currentStats,
                    completed: currentStats.completed + (completed ? 1 : -1),
                    pending: currentStats.pending + (completed ? -1 : 1)
                }
            },
            false
        );

        // 3. Update Today's Tasks Optimistically
        mutate(
            `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/today?limit=5`,
            (data: { tasks: Task[], count: number } | undefined) => {
                if (!data) return undefined;
                return {
                    ...data,
                    tasks: data.tasks.map(t => t.id === taskId ? { ...t, completed } : t),
                    count: data.count // Count doesn't change on toggle
                };
            },
            false
        );

        try {
            const token = await getJWTToken();
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/tasks/${taskId}/complete`,
                {
                    method: 'PATCH',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                }
            );

            if (!response.ok) throw new Error('Failed');

            // Revalidate all to ensure server sync
            refreshAll();
        } catch (error) {
            // Revert on error
            refreshAll();
            toast.error('Failed to update task');
        }
    };

    const updateTask = async (task: Task) => {
        if (!user?.id) return;

        // 1. Update Tasks List
        mutate(
            `${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/tasks`,
            (currentTasks: Task[] | undefined) => {
                if (!currentTasks) return [];
                return currentTasks.map(t => t.id === task.id ? task : t);
            },
            false
        );

        // 2. Update Today's Tasks
        mutate(
            `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/today?limit=5`,
            (data: { tasks: Task[], count: number } | undefined) => {
                if (!data) return undefined;
                return {
                    ...data,
                    tasks: data.tasks.map(t => t.id === task.id ? task : t),
                    count: data.count
                };
            },
            false
        );

        // 3. Recalculate Stats - just revalidate to be safe if content changed drastically
        // mutate(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/stats`); 
    };

    const deleteTask = async (taskId: number) => {
        if (!user?.id) return;

        // 1. Update Tasks List
        mutate(
            `${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/tasks`,
            (currentTasks: Task[] | undefined) => {
                if (!currentTasks) return [];
                return currentTasks.filter(t => t.id !== taskId);
            },
            false
        );

        // 2. Update Today's Tasks
        mutate(
            `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/today?limit=5`,
            (data: { tasks: Task[], count: number } | undefined) => {
                if (!data) return undefined;
                return {
                    ...data,
                    tasks: data.tasks.filter(t => t.id !== taskId),
                    count: Math.max(0, data.count - 1)
                };
            },
            false
        );

        // 3. Stats - revalidate because we don't know the state of deleted task easily
        // ... (existing deleteTask code)
        mutate(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/stats`);
    };

    const createTask = async (newTask: Task) => {
        if (!user?.id) return;

        // 1. Update Tasks List
        mutate(
            `${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/tasks`,
            (currentTasks: Task[] | undefined) => {
                return currentTasks ? [newTask, ...currentTasks] : [newTask];
            },
            false
        );

        // 2. Update Today's Tasks (if it belongs to today)
        // We assume created tasks are for today unless specified otherwise.
        mutate(
            `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/today?limit=5`,
            (data: { tasks: Task[], count: number } | undefined) => {
                if (!data) return undefined;
                // Check if already in list to avoid duplicates if revalidated quickly
                if (data.tasks.find(t => t.id === newTask.id)) return data;

                return {
                    ...data,
                    tasks: [newTask, ...data.tasks].slice(0, 5), // Maintain limit
                    count: data.count + 1
                };
            },
            false
        );

        // 3. Update Stats
        mutate(
            `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/stats`,
            (currentStats: any) => {
                if (!currentStats) return { total: 0, completed: 0, pending: 0 };
                return {
                    ...currentStats,
                    total: currentStats.total + 1,
                    pending: currentStats.pending + 1 // New tasks are pending
                };
            },
            false
        );

        // 4. Update Category Stats (increment count for the task's category)
        if (newTask.category_id) {
            mutate(
                `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/stats/categories`,
                (currentStats: any[] | undefined) => {
                    if (!currentStats) return undefined;
                    return currentStats.map((cat: any) =>
                        cat.category_id === newTask.category_id
                            ? { ...cat, count: cat.count + 1 }
                            : cat
                    );
                },
                false
            );
        }

        // 5. Revalidate all caches from server to ensure consistency across pages
        refreshAll();
    };

    return {
        refreshAll,
        updateTaskCompletion,
        updateTask,
        deleteTask,
        createTask
    };
}
