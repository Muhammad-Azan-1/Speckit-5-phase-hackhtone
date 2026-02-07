'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuth } from '@/hooks/use-auth'
import { CreateTaskData } from '@/types/task'
import { toast } from 'sonner'
import { getJWTToken } from '@/lib/auth-client'
import { useCategories } from '@/hooks/use-tasks'

interface TaskFormProps {
  onTaskCreated: (task: any) => void
}

export function TaskForm({ onTaskCreated }: TaskFormProps) {
  const { user } = useAuth()
  const [formData, setFormData] = useState<CreateTaskData & { category_id?: number }>({ title: '', description: '' })
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})

  // Use shared SWR hook for categories (instant updates when deleted elsewhere)
  const { categories, isLoading: loadingCategories } = useCategories()

  const validate = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required'
    } else if (formData.title.length < 1 || formData.title.length > 200) {
      newErrors.title = 'Title must be between 1 and 200 characters'
    }

    if (!formData.description?.trim()) {
      newErrors.description = 'Description is required'
    } else if (formData.description.length > 1000) {
      newErrors.description = 'Description must be less than 1000 characters'
    }

    setErrors(newErrors)

    // Auto-clear errors after 3 seconds
    if (Object.keys(newErrors).length > 0) {
      setTimeout(() => setErrors({}), 3000)
    }

    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validate() || !user?.id) {
      return
    }

    setLoading(true)
    try {
      // Get fresh JWT token
      const { authClient } = await import('@/lib/auth-client')
      const tokenResponse = await authClient.token()
      const token = tokenResponse.data?.token

      if (!token) throw new Error('Authentication token missing')

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: formData.title,
          description: formData.description || null,
          category_id: formData.category_id || null,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail?.message || `Failed to create task: ${response.status}`)
      }

      const newTask = await response.json()
      onTaskCreated(newTask)
      setFormData({ title: '', description: '', category_id: undefined }) // Reset form
    } catch (err: any) {
      console.error('Error creating task:', err)
      toast.error(err.message || 'Failed to create task')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'category_id' ? (value ? parseInt(value) : undefined) : value
    }))
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Create New Task</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="title" className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Title *
            </label>
            <Input
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Task title"
              disabled={loading}
              className={errors.title ? "border-red-500" : ""}
            />
            {errors.title && <p className="text-red-500 text-sm">{errors.title}</p>}
          </div>

          <div className="space-y-2">
            <label htmlFor="description" className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Description *
            </label>
            <Textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Task description"
              disabled={loading}
              className={errors.description ? "border-red-500" : ""}
            />
            {errors.description && <p className="text-red-500 text-sm">{errors.description}</p>}
          </div>

          <div className="space-y-2">
            <label htmlFor="category_id" className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Category
            </label>
            <select
              id="category_id"
              name="category_id"
              value={formData.category_id || ''}
              onChange={handleChange}
              disabled={loading || loadingCategories}
              className="w-full p-2 border rounded-md bg-background text-foreground"
            >
              <option value="">No Category</option>
              {categories.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.icon} {cat.name}
                </option>
              ))}
            </select>
          </div>

          <Button
            type="submit"
            className="w-full"
            disabled={loading}
          >
            {loading ? 'Creating...' : 'Create Task'}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}