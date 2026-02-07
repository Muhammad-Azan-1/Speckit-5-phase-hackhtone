import React from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';

interface AuthCardProps {
  title: string;
  description?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export function AuthCard({ title, description, children, footer }: AuthCardProps) {
  return (
    <Card className="w-full max-w-md mx-auto overflow-hidden border border-gray-200 shadow-xl bg-white dark:bg-gray-800 transition-all duration-300 hover:shadow-2xl">
      <CardHeader className="space-y-1 text-center py-8 px-8">
        <CardTitle className="text-2xl font-bold text-gray-900 dark:text-white">
          {title}
        </CardTitle>
        {description && (
          <CardDescription className="text-gray-600 dark:text-gray-300 mt-2 text-sm">
            {description}
          </CardDescription>
        )}
      </CardHeader>
      <CardContent className="px-8 pb-6">
        {children}
      </CardContent>
      {footer && (
        <CardFooter className="justify-center pb-6">
          {footer}
        </CardFooter>
      )}
    </Card>
  );
}