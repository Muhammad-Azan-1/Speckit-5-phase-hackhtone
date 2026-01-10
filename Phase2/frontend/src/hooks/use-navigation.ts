import { useState } from 'react';

export function useNavigation() {
  const [activePage, setActivePage] = useState('');

  const navigateTo = (page: string) => {
    setActivePage(page);
    // In a real app, this would use router.push
    window.location.hash = page;
  };

  return {
    activePage,
    setActivePage,
    navigateTo,
  };
}