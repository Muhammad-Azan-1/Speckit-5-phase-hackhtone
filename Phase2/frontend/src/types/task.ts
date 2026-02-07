export interface Task {
  id: number
  title: string
  description?: string
  completed: boolean
  user_id: string
  category_id?: number
  category_name?: string
  version: number
  created_at: string
  updated_at: string
}

export interface CreateTaskData {
  title: string
  description?: string
  category_id?: number
}

export interface UpdateTaskData {
  title?: string
  description?: string
  completed?: boolean
  category_id?: number
  version?: number
}