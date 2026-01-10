import { useState, useEffect } from 'react';
import { dashboardAPI, categoryAPI } from '@/lib/api';

interface TaskStats {
  total: number;
  completed: number;
  pending: number;
}

interface CategoryStats {
  category_id: number;
  name: string;
  icon: string;
  count: number;
}

interface TodayTask {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  category_id?: number;
  due_time?: string;
  created_at: string;
  updated_at: string;
}

interface TodayTasksResponse {
  tasks: TodayTask[];
  count: number;
}

interface DashboardData {
  stats: TaskStats | null;
  categories: CategoryStats[];
  todayTasks: TodayTask[];
  loading: boolean;
  error: string | null;
}

export function useDashboard() {
  const [data, setData] = useState<DashboardData>({
    stats: null,
    categories: [],
    todayTasks: [],
    loading: true,
    error: null,
  });

  const fetchData = async () => {
    setData(prev => ({ ...prev, loading: true, error: null }));

    try {
      // Fetch all dashboard data in parallel
      const [statsResponse, categoriesResponse, todayTasksResponse] = await Promise.all([
        dashboardAPI.getTaskStats(),
        dashboardAPI.getCategoryStats(),
        dashboardAPI.getTodayTasks(5)
      ]);

      const stats: TaskStats = statsResponse.data;
      const categories: CategoryStats[] = categoriesResponse.data;
      const todayTasksResponseData: TodayTasksResponse = todayTasksResponse.data;

      setData({
        stats,
        categories,
        todayTasks: todayTasksResponseData.tasks,
        loading: false,
        error: null,
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setData({
        stats: null,
        categories: [],
        todayTasks: [],
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to load dashboard data',
      });
    }
  };

  // Fetch data on mount
  useEffect(() => {
    fetchData();
  }, []);

  return {
    ...data,
    refetch: fetchData,
  };
}