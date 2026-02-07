'use client';

import { useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Skeleton } from '@/components/ui/skeleton';
import { Clock, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useSession } from '@/lib/auth-client';
import { useTodayTasks, useTaskMutations } from '@/hooks/use-tasks';
import { useUserPreferences } from '@/hooks/use-user';

interface TodayTasksProps {
  onTaskToggle?: (wasCompleted: boolean) => void;
}

export function TodayTasksComponent({ onTaskToggle }: TodayTasksProps = {}) {
  const { data: session } = useSession();
  const { tasks, isLoading, mutate } = useTodayTasks(5);
  const { updateTaskCompletion } = useTaskMutations();
  const { preferences } = useUserPreferences();

  // Filter tasks based on show_completed_tasks preference
  const filteredTasks = useMemo(() => {
    if (!preferences?.show_completed_tasks) {
      return tasks.filter(task => !task.completed);
    }
    return tasks;
  }, [tasks, preferences?.show_completed_tasks]);

  const handleToggleComplete = async (taskId: number) => {
    if (!session?.user?.id) return;

    const taskToUpdate = tasks.find(t => t.id === taskId);
    if (!taskToUpdate) return;

    // Use centralized mutation handler which handles all optimistic updates and cache syncing
    await updateTaskCompletion(taskId, !taskToUpdate.completed);

    // Legacy support for parent component stats update if needed
    onTaskToggle?.(taskToUpdate.completed);
  };

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Today's Tasks</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="flex items-center space-x-4 p-3 border rounded-lg">
                <Skeleton className="h-5 w-5 rounded" />
                <div className="flex-1">
                  <Skeleton className="h-4 w-48 mb-2" />
                  <Skeleton className="h-3 w-24" />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Today's Tasks</CardTitle>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => {
            mutate();
          }}
          title="Refresh tasks"
        >
          <RefreshCw className="h-4 w-4" />
        </Button>
      </CardHeader>
      <CardContent>
        {filteredTasks.length === 0 ? (
          <p className="text-muted-foreground text-center py-4">
            No tasks created today. Start by adding a new task!
          </p>
        ) : (
          <div className="space-y-3">
            {filteredTasks.map((task) => (
              <div
                key={task.id}
                className="flex items-center space-x-4 p-3 border rounded-lg hover:bg-accent/50 transition-colors"
              >
                <Checkbox
                  checked={task.completed}
                  onCheckedChange={() => handleToggleComplete(task.id)}
                  aria-label={`Toggle completion for ${task.title}`}
                />
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className={`${task.completed ? 'line-through text-muted-foreground' : ''}`}>
                      {task.title}
                    </span>
                  </div>
                  {task.description && (
                    <p className="text-sm text-muted-foreground mt-1 line-clamp-1">
                      {task.description}
                    </p>
                  )}
                </div>
                <div className="flex items-center text-sm text-muted-foreground">
                  <Clock className="h-4 w-4 mr-1" />
                  {new Date(task.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}