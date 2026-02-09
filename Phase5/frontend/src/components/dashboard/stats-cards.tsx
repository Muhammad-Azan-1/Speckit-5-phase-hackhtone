'use client';

import { useImperativeHandle, forwardRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { TrendingUp, CheckCircle, Circle } from 'lucide-react';
import { useStats } from '@/hooks/use-tasks';

interface StatCardProps {
  title: string;
  value: string;
  icon: React.ReactNode;
  loading?: boolean;
}

export interface StatsCardsRef {
  refresh: () => void;
  updateStats: (delta: { completed?: number; pending?: number }) => void;
}

const StatCard = ({ title, value, icon, loading }: StatCardProps) => {
  if (loading) {
    return (
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">{title}</CardTitle>
          {icon}
        </CardHeader>
        <CardContent>
          <Skeleton className="h-8 w-16" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
      </CardContent>
    </Card>
  );
};

export const StatsCardsComponent = forwardRef<StatsCardsRef>((_, ref) => {
  const { stats, isLoading, mutate } = useStats();

  // Expose refresh and updateStats methods via ref
  useImperativeHandle(ref, () => ({
    refresh: () => mutate(),
    updateStats: (delta: { completed?: number; pending?: number }) => {
      mutate({
        ...stats,
        completed: stats.completed + (delta.completed || 0),
        pending: stats.pending + (delta.pending || 0),
      }, false); // Update locally without revalidating immediately
    },
  }));

  return (
    <>
      <StatCard
        title="Total Tasks"
        value={stats?.total?.toString() || '0'}
        icon={<TrendingUp className="h-4 w-4 text-muted-foreground" />}
        loading={isLoading}
      />
      <StatCard
        title="Completed"
        value={stats?.completed?.toString() || '0'}
        icon={<CheckCircle className="h-4 w-4 text-green-500" />}
        loading={isLoading}
      />
      <StatCard
        title="Pending"
        value={stats?.pending?.toString() || '0'}
        icon={<Circle className="h-4 w-4 text-orange-500" />}
        loading={isLoading}
      />
    </>
  );
});

StatsCardsComponent.displayName = 'StatsCardsComponent';