'use client'

import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

interface TaskFilterProps {
  filter: 'all' | 'pending' | 'completed'
  onFilterChange: (filter: 'all' | 'pending' | 'completed') => void
  sortBy: 'created' | 'title'
  onSortChange: (sortBy: 'created' | 'title') => void
  sortOrder: 'asc' | 'desc'
  onSortOrderChange: (sortOrder: 'asc' | 'desc') => void
}

export function TaskFilter({
  filter,
  onFilterChange,
  sortBy,
  onSortChange,
  sortOrder,
  onSortOrderChange
}: TaskFilterProps) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      {/* Filter buttons - consistent sizing */}
      <div className="flex gap-1">
        <Button
          variant={filter === 'all' ? 'default' : 'outline'}
          size="sm"
          onClick={() => onFilterChange('all')}
          className="h-9 min-w-[60px] justify-center"
        >
          All
        </Button>
        <Button
          variant={filter === 'pending' ? 'default' : 'outline'}
          size="sm"
          onClick={() => onFilterChange('pending')}
          className="h-9 min-w-[80px] justify-center"
        >
          Pending
        </Button>
        <Button
          variant={filter === 'completed' ? 'default' : 'outline'}
          size="sm"
          onClick={() => onFilterChange('completed')}
          className="h-9 min-w-[80px] justify-center"
        >
          Completed
        </Button>
      </div>

      {/* Sort dropdowns - matching height */}
      <Select value={sortBy} onValueChange={(value: 'created' | 'title') => onSortChange(value)}>
        <SelectTrigger className="h-9 w-[130px]">
          <SelectValue placeholder="Sort by..." />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="created">Sort by Date</SelectItem>
          <SelectItem value="title">Sort by Title</SelectItem>
        </SelectContent>
      </Select>

      <Select value={sortOrder} onValueChange={(value: 'asc' | 'desc') => onSortOrderChange(value)}>
        <SelectTrigger className="h-9 w-[120px]">
          <SelectValue placeholder="Order..." />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="asc">Ascending</SelectItem>
          <SelectItem value="desc">Descending</SelectItem>
        </SelectContent>
      </Select>
    </div>
  )
}