'use client'

import { useState } from 'react'
import { Task } from '@/types/task'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardFooter } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Badge } from '@/components/ui/badge'
import { useAuth } from '@/hooks/use-auth'
import { toast } from 'sonner'
import { useTaskMutations } from '@/hooks/use-tasks'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'

interface TaskItemProps {
  task: Task
  onTaskUpdated: (task: Task) => void
  onTaskDeleted: (taskId: number) => void
}

export function TaskItem({ task, onTaskUpdated, onTaskDeleted }: TaskItemProps) {
  const { user } = useAuth()
  const { updateTaskCompletion, updateTask, deleteTask } = useTaskMutations()
  const [isEditing, setIsEditing] = useState(false)
  const [title, setTitle] = useState(task.title)
  const [description, setDescription] = useState(task.description || '')
  const [isLoading, setIsLoading] = useState(false)
  const [localCompleted, setLocalCompleted] = useState(task.completed)

  const handleToggleComplete = async () => {
    if (!user?.id) return

    // Optimistic update for local UI
    const previousState = localCompleted
    setLocalCompleted(!localCompleted)

    // Call centralized mutation handler which updates all caches AND performs API Call
    await updateTaskCompletion(task.id, !localCompleted)
  }

  const handleDelete = async () => {
    if (!user?.id) return

    setIsLoading(true)

    // Optimistic Delete
    // We can call deleteTask from hook to update UI immediately
    await deleteTask(task.id)
    onTaskDeleted(task.id)

    try {
      const { authClient } = await import('@/lib/auth-client')
      const tokenResponse = await authClient.token()
      const token = tokenResponse.data?.token
      if (!token) throw new Error('Authentication token missing')

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/tasks/${task.id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail?.message || `Failed to delete task: ${response.status}`)
      }

      toast.success('Task deleted successfully!')
    } catch (err: any) {
      console.error('Error deleting task:', err)
      toast.error(err.message || 'Failed to delete task')
      // Revert if needed, but for delete it's rare. Ideally we'd refreshAll() here.
    } finally {
      setIsLoading(false)
    }
  }

  const handleSaveEdit = async () => {
    if (!user?.id) return

    setIsLoading(true)

    const updatedTaskContent = {
      ...task,
      title,
      description,
      completed: localCompleted,
      // version is handled by backend or needs to be passed
    }

    // Optimistic Update
    await updateTask(updatedTaskContent)

    try {
      const { authClient } = await import('@/lib/auth-client')
      const tokenResponse = await authClient.token()
      const token = tokenResponse.data?.token
      if (!token) throw new Error('Authentication token missing')

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/tasks/${task.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          title,
          description,
          completed: localCompleted,
          version: task.version
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail?.message || `Failed to update task: ${response.status}`)
      }

      const updatedTaskServer = await response.json()

      // Confirm update with server data
      await updateTask(updatedTaskServer)
      onTaskUpdated(updatedTaskServer)

      setIsEditing(false)
      toast.success('Task updated successfully!')
    } catch (err: any) {
      console.error('Error saving task:', err)
      if (err.message.includes('409')) {
        toast.error('Task was modified by another user. Please refresh and try again.')
      } else {
        toast.error(err.message || 'Failed to update task')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <Card className={`${localCompleted ? 'opacity-70' : ''}`}>
      <CardContent className="pt-6">
        <div className="flex items-start gap-4">
          <div className="mt-1">
            <Checkbox
              checked={localCompleted}
              onCheckedChange={handleToggleComplete}
              disabled={isLoading}
            />
          </div>

          <div className="flex-1 min-w-0">
            {isEditing ? (
              <div className="space-y-3">
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full text-lg font-semibold bg-transparent border-b border-gray-300 focus:outline-none focus:border-blue-500"
                  disabled={isLoading}
                />
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full bg-transparent border-b border-gray-300 focus:outline-none focus:border-blue-500 resize-none"
                  disabled={isLoading}
                />
              </div>
            ) : (
              <div>
                <h3 className={`text-lg font-semibold ${localCompleted ? 'line-through' : ''}`}>
                  {task.title}
                </h3>
                {task.description && (
                  <p className={`mt-1 text-gray-600 dark:text-gray-400 ${localCompleted ? 'line-through' : ''}`}>
                    {task.description}
                  </p>
                )}
              </div>
            )}

            <div className="mt-2 flex flex-wrap items-center gap-2">
              <Badge variant={localCompleted ? 'default' : 'secondary'}>
                {localCompleted ? 'Completed' : 'Pending'}
              </Badge>
              {task.category_name && (
                <Badge variant="outline">
                  {task.category_name}
                </Badge>
              )}
              <span className="text-xs text-gray-500 dark:text-gray-400">
                Created: {formatDate(task.created_at)}
              </span>
              {task.updated_at !== task.created_at && (
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  Updated: {formatDate(task.updated_at)}
                </span>
              )}
            </div>
          </div>
        </div>
      </CardContent>

      <CardFooter className="flex justify-between">
        <div className="flex gap-2">
          {isEditing ? (
            <>
              <Button size="sm" onClick={handleSaveEdit} disabled={isLoading}>
                {isLoading ? 'Saving...' : 'Save'}
              </Button>
              <Button size="sm" variant="outline" onClick={() => setIsEditing(false)} disabled={isLoading}>
                Cancel
              </Button>
            </>
          ) : (
            <Button size="sm" variant="outline" onClick={() => setIsEditing(true)} disabled={isLoading}>
              Edit
            </Button>
          )}
        </div>

        <div className="flex gap-2">
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button size="sm" variant="destructive" disabled={isLoading}>
                Delete
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Delete Task</AlertDialogTitle>
                <AlertDialogDescription>
                  Are you sure you want to delete "{task.title}"? This action cannot be undone.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction onClick={handleDelete} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                  Delete
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </CardFooter>
    </Card>
  )
}