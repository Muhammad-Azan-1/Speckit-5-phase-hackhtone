'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { useCategoryStats } from '@/hooks/use-tasks';

interface CategoryItem {
  category_id: number;
  name: string;
  icon: string;
  count: number;
}

export function CategoriesSectionComponent() {
  const { categoryStats: categories, isLoading } = useCategoryStats();

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Categories</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex flex-col items-center text-center">
                <Skeleton className="h-8 w-8 rounded-full mb-1" />
                <Skeleton className="h-4 w-16 mb-1" />
                <Skeleton className="h-5 w-8" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (categories.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Categories</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-center py-4">
            No categories yet. Create categories in Settings to organize your tasks.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Categories</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
          {categories.map((category: CategoryItem) => (
            <div key={category.category_id} className="flex flex-col items-center text-center p-3 rounded-lg hover:bg-accent/50 transition-colors cursor-pointer">
              <span className="text-2xl mb-1">{category.icon}</span>
              <span className="font-medium text-sm">{category.name}</span>
              <Badge variant="secondary" className="mt-1">
                {category.count} {category.count === 1 ? 'task' : 'tasks'}
              </Badge>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}