'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface GreetingComponentProps {
  userName?: string;
}

export function GreetingComponent({ userName }: GreetingComponentProps) {
  const [currentTime, setCurrentTime] = useState(new Date());

  // Update time every minute
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 60000);
    return () => clearInterval(timer);
  }, []);

  const hour = currentTime.getHours();

  // Time-based greeting and emoji
  let greeting = 'Good evening';
  let emoji = '🌙';

  if (hour >= 5 && hour < 12) {
    greeting = 'Good morning';
    emoji = '☀️';
  } else if (hour >= 12 && hour < 17) {
    greeting = 'Good afternoon';
    emoji = '🌤️';
  } else if (hour >= 17 && hour < 21) {
    greeting = 'Good evening';
    emoji = '🌅';
  } else {
    greeting = 'Good night';
    emoji = '🌙';
  }

  // Format time as HH:MM AM/PM
  const formattedTime = currentTime.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });

  // Format date
  const formattedDate = currentTime.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric'
  });

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold">{greeting}, {userName}! {emoji}</h1>
            <p className="text-muted-foreground mt-1">{formattedDate}</p>
          </div>
          <Badge variant="secondary" className="text-sm px-3 py-1">
            {formattedTime}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}