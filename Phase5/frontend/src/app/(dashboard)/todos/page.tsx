'use client'

import { useState, useMemo, useEffect } from 'react'
import { TaskList } from '@/components/todos/task-list'
import { TaskForm } from '@/components/todos/task-form'
import { useAuth } from '@/hooks/use-auth'
import { Task } from '@/types/task'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Search, ArrowUp } from 'lucide-react'
import { useTasks, useTaskMutations } from '@/hooks/use-tasks'
import { Skeleton } from '@/components/ui/skeleton'
import { useUserPreferences } from '@/hooks/use-user'

export default function TodosPage() {
  const { user } = useAuth()
  const { tasks, isLoading, isError, mutate } = useTasks()
  const { createTask, updateTask, deleteTask } = useTaskMutations()
  const { preferences } = useUserPreferences()

  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState<'all' | 'pending' | 'completed'>('all')
  const [categoryFilter, setCategoryFilter] = useState<string>('all')
  const [showScrollTop, setShowScrollTop] = useState(false)

  // Track scroll position to show/hide scroll-to-top button
  // Dashboard layout uses overflow-y-auto on main, so we track that instead of window
  useEffect(() => {
    const mainElement = document.querySelector('main')
    if (!mainElement) return

    const handleScroll = () => {
      setShowScrollTop(mainElement.scrollTop > 300)
    }
    mainElement.addEventListener('scroll', handleScroll)
    return () => mainElement.removeEventListener('scroll', handleScroll)
  }, [])

  const scrollToTop = () => {
    const mainElement = document.querySelector('main')
    mainElement?.scrollTo({ top: 0, behavior: 'smooth' })
  }

  // Derived state for filtered tasks
  const filteredTasks = useMemo(() => {
    let result = [...tasks]

    // Apply show_completed_tasks preference (hide completed if toggle is off)
    if (!preferences?.show_completed_tasks) {
      result = result.filter(task => !task.completed)
    }

    // Apply manual status filter
    if (statusFilter !== 'all') {
      result = result.filter(task =>
        statusFilter === 'completed' ? task.completed : !task.completed
      )
    }
    if (searchTerm) {
      result = result.filter(task =>
        task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase()))
      )
    }
    if (categoryFilter !== 'all') {
      result = result.filter(task =>
        task.category_name && task.category_name.toLowerCase() === categoryFilter.toLowerCase()
      )
    }
    return result
  }, [tasks, searchTerm, statusFilter, categoryFilter, preferences?.show_completed_tasks])

  const handleTaskCreated = async (newTask: Task) => {
    // use centralized mutation to update all caches (dashboard, stats, tasks)
    await createTask(newTask)
    toast.success('Task created successfully!')
  }

  const handleTaskUpdated = (updatedTask: Task) => {
    // TaskItem already calls updateTask from hook, so we might not need to do anything here
    // But if TaskForm or other components call this directly without hook, we should ensure hook is used.
    // However, TaskItem uses the hook. TaskList passes this handler to TaskItem.
    // TaskItem calls: onTaskUpdated(updatedTask).
    // So this function is just for local UI feedback if needed, but cache is already updated by TaskItem.
    // We can leave it empty or remove manual mutation.
  }

  const handleTaskDeleted = (taskId: number) => {
    // TaskItem already calls deleteTask from hook.
  }

  if (!user) {
    return <div>Please log in to view your tasks</div>
  }

  if (isLoading) {
    return (
      <div className="container mx-auto py-8">
        <Skeleton className="h-10 w-48 mb-8" />
        <div className="flex gap-2 mb-6">
          <Skeleton className="h-9 w-24" />
          <Skeleton className="h-9 w-24" />
          <Skeleton className="h-9 w-24" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-4">
            {[...Array(3)].map((_, i) => (
              <Skeleton key={i} className="h-24 w-full" />
            ))}
          </div>
          <div>
            <Skeleton className="h-64 w-full" />
          </div>
        </div>
      </div>
    )
  }

  if (isError) {
    return <div className="text-red-500 p-4">Failed to load tasks</div>
  }

  // Get unique categories from tasks
  const uniqueCategories = Array.from(
    new Set(tasks.map(task => task.category_name).filter(Boolean) as string[])
  )

  return (
    <div className="container mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">My Tasks</h1>
        <p className="text-gray-600 dark:text-gray-400">Manage your to-do items</p>
      </div>

      {/* Filter tabs - consistent sizing */}
      <div className="flex flex-wrap gap-2 mb-6">
        <Button
          variant={statusFilter === 'all' ? 'secondary' : 'outline'}
          size="sm"
          onClick={() => setStatusFilter('all')}
          className="h-9 min-w-[100px] justify-center"
        >
          All: {tasks.length}
        </Button>
        <Button
          variant={statusFilter === 'pending' ? 'secondary' : 'outline'}
          size="sm"
          onClick={() => setStatusFilter('pending')}
          className="h-9 min-w-[100px] justify-center"
        >
          Pending: {tasks.filter(t => !t.completed).length}
        </Button>
        <Button
          variant={statusFilter === 'completed' ? 'secondary' : 'outline'}
          size="sm"
          onClick={() => setStatusFilter('completed')}
          className="h-9 min-w-[100px] justify-center"
        >
          Completed: {tasks.filter(t => t.completed).length}
        </Button>
      </div>

      {/* Search bar with category filter */}
      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search tasks..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-10 pr-32"
        />
        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="absolute right-2 top-1/2 transform -translate-y-1/2 h-8 px-2 text-sm bg-transparent border-0 focus:ring-0 focus:outline-none"
        >
          <option value="all">All Categories</option>
          {uniqueCategories.map(category => (
            <option key={category} value={category}>{category}</option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <TaskList
            tasks={filteredTasks}
            onTaskUpdated={handleTaskUpdated}
            onTaskDeleted={handleTaskDeleted}
          />
        </div>
        <div className="lg:sticky lg:top-4 lg:self-start">
          <TaskForm onTaskCreated={handleTaskCreated} />
        </div>
      </div>

      {/* Scroll to Top Button */}
      {showScrollTop && (
        <Button
          onClick={scrollToTop}
          className="fixed bottom-6 right-6 rounded-full w-12 h-12 shadow-lg z-50 transition-all duration-300 hover:scale-110"
          size="icon"
          aria-label="Scroll to top"
        >
          <ArrowUp className="h-5 w-5" />
        </Button>
      )}
    </div>
  )
}