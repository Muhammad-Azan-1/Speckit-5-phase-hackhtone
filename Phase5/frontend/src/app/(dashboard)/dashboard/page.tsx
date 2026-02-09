'use client';

import { useRef } from 'react';
import { useSession } from '@/lib/auth-client';
import { GreetingComponent } from '@/components/dashboard/greeting';
import { StatsCardsComponent, StatsCardsRef } from '@/components/dashboard/stats-cards';
import { CategoriesSectionComponent } from '@/components/dashboard/categories-section';
import { TodayTasksComponent } from '@/components/dashboard/today-tasks';

export default function DashboardPage() {
  const { data: session, isPending } = useSession();
  const statsRef = useRef<StatsCardsRef>(null);



  if (isPending) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="flex flex-col items-center justify-center h-64">
        <h1 className="text-2xl font-bold">Access Denied</h1>
        <p className="text-muted-foreground">Please sign in to access the dashboard</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Greeting */}
      <div>
        <GreetingComponent userName={session.user?.name || 'User'} />
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCardsComponent ref={statsRef} />
      </div>

      {/* Categories Section */}
      <div>
        <CategoriesSectionComponent />
      </div>

      {/* Today's Tasks */}
      <div>
        <TodayTasksComponent />
      </div>
    </div>
  );
}