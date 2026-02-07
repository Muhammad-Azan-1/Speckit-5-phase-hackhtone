'use client'

import { useState } from 'react'
import { TaskItem } from './task-item'
import { Task } from '@/types/task'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { EmptyState } from '../ui/empty-state'
import { TaskFilter } from './task-filter'

interface TaskListProps {
  tasks: Task[]
  onTaskUpdated: (task: Task) => void
  onTaskDeleted: (taskId: number) => void
}

export function TaskList({ tasks, onTaskUpdated, onTaskDeleted }: TaskListProps) {
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all')
  const [sortBy, setSortBy] = useState<'created' | 'title'>('created')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc')

  // Filter tasks based on the selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'pending') return !task.completed
    if (filter === 'completed') return task.completed
    return true // 'all' filter
  })

  // Sort tasks
  const sortedTasks = [...filteredTasks].sort((a, b) => {
    if (sortBy === 'title') {
      return sortOrder === 'asc'
        ? a.title.localeCompare(b.title)
        : b.title.localeCompare(a.title)
    } else { // sortBy === 'created'
      const dateA = new Date(a.created_at).getTime()
      const dateB = new Date(b.created_at).getTime()
      return sortOrder === 'asc' ? dateA - dateB : dateB - dateA
    }
  })

  const pendingCount = tasks.filter(task => !task.completed).length
  const completedCount = tasks.filter(task => task.completed).length

  if (tasks.length === 0) {
    return (
      <EmptyState
        title="No tasks yet"
        description="Create your first task to get started"
        action={
          <Button onClick={() => window.location.reload()}>
            Refresh
          </Button>
        }
      />
    )
  }

  return (
    <Card>
      <CardHeader className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <CardTitle>Your Tasks</CardTitle>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {tasks.length} total, {pendingCount} pending, {completedCount} completed
          </p>
        </div>
        <TaskFilter
          filter={filter}
          onFilterChange={setFilter}
          sortBy={sortBy}
          onSortChange={setSortBy}
          sortOrder={sortOrder}
          onSortOrderChange={setSortOrder}
        />
      </CardHeader>
      <CardContent>
        {sortedTasks.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500 dark:text-gray-400">
              No {filter} tasks found. Try changing your filter.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {sortedTasks.map(task => (
              <TaskItem
                key={task.id}
                task={task}
                onTaskUpdated={onTaskUpdated}
                onTaskDeleted={onTaskDeleted}
              />
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}