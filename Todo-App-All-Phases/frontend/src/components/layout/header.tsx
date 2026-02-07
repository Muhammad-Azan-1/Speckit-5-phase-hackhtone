'use client'

import { UserNav } from './user-nav'
import { Sidebar } from './sidebar'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Button } from '@/components/ui/button'
import { Menu } from 'lucide-react'
import { useState } from 'react'

export default function Header() {
    const [open, setOpen] = useState(false)

    return (
        <header className="border-b bg-white dark:bg-gray-950 px-6 py-3 flex items-center justify-between sticky top-0 z-10">
            <div className="flex items-center gap-4 lg:hidden">
                <Sheet open={open} onOpenChange={setOpen}>
                    <SheetTrigger asChild>
                        <Button variant="ghost" size="icon" className="lg:hidden">
                            <Menu className="h-6 w-6" />
                        </Button>
                    </SheetTrigger>
                    <SheetContent side="left" className="p-0">
                        <Sidebar mobile onClose={() => setOpen(false)} />
                    </SheetContent>
                </Sheet>
                <span className="font-bold text-lg">Todo App</span>
            </div>

            <div className="hidden lg:block">
                {/* Desktop Title if needed or Breadcrumbs */}
            </div>

            <div className="flex items-center gap-4 ml-auto">
                <UserNav />
            </div>
        </header>
    )
}
